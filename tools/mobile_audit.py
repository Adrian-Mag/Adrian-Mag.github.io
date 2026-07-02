#!/usr/bin/env python3
"""
Mobile-width audit: find the blocking element on every HTML page at 360px.

For each page, it:
  1. Loads the page at 360x900 viewport
  2. Waits for MathJax/Plotly to settle
  3. Measures every element's scrollWidth vs clientWidth and bounding rect
  4. Reports the deepest element that overflows (the "blocking element")

Usage:
    python3 tools/mobile_audit.py [--width 360] [--json]
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

# ── Config ──────────────────────────────────────────────────────────────

TARGET_WIDTH = 360
TARGET_HEIGHT = 900
SETTLE_TIMEOUT = 8000  # ms to wait for MathJax/Plotly

ROOT = Path(__file__).resolve().parent.parent

# Pages to skip (login, temp, generated)
SKIP_PATTERNS = {
    "output.html",
    "papers-login.html",
    "sola-login.html",
    "papers-in-prep.html",
}

# ── JS to run in page ───────────────────────────────────────────────────

AUDIT_JS = r"""
() => {
    const vw = document.documentElement.clientWidth;

    function label(el) {
        const id = el.id ? `#${el.id}` : "";
        const cls =
            typeof el.className === "string" && el.className.trim()
                ? "." + el.className.trim().replace(/\s+/g, ".")
                : "";
        return `${el.tagName.toLowerCase()}${id}${cls}`;
    }

    function path(el) {
        const parts = [];
        let cur = el;
        while (cur && cur !== document.body) {
            parts.unshift(label(cur));
            cur = cur.parentElement;
        }
        return parts.join(" > ");
    }

    const results = [];
    const all = document.querySelectorAll("body *");

    for (const el of all) {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);

        // Skip elements with zero size (display:none, etc.)
        if (rect.width === 0 && rect.height === 0) continue;

        // Skip hidden accessibility elements (MathJax assistive MathML)
        if (el.tagName.toLowerCase() === "mjx-assistive-mml" ||
            el.tagName.toLowerCase() === "math") continue;

        const tag = el.tagName.toLowerCase();

        // Skip MathML elements — children of the hidden mjx-assistive-mml
        const mathmlTags = ["mo","mi","mn","ms","mtext","mrow","mfrac",
            "msup","msub","msubsup","menclose","munder","mover",
            "munderover","mtable","mtr","mtd","mspace","mphantom",
            "mpadded","mstyle","merror","mfenced","mroot","msqrt"];
        if (mathmlTags.includes(tag)) continue;

        // Skip internal MathJax rendering elements — they're contained
        // within the scrollable mjx-container and don't cause visible overflow
        if (tag.startsWith("mjx-") && tag !== "mjx-container") continue;

        const overflowRight = rect.right - vw;
        const overflowLeft = -rect.left;
        const internalOverflow = el.scrollWidth - el.clientWidth;

        // Determine if internal overflow is a real problem:
        // - overflow-x: auto → intentional scrolling, NOT a problem
        // - overflow-x: hidden → content is clipped (problem)
        // - overflow-x: visible → content escapes (problem if it pushes layout)
        const overflowX = style.overflowX;
        const internalIsProblem = internalOverflow > 3 && overflowX !== "auto";

        // Element is a problem if:
        // 1. It extends beyond the viewport (overflowRight > 1)
        // 2. It has CLIPPING internal overflow (overflow-x: hidden/visible)
        // 3. It's pushed left off-screen (overflowLeft > 1)
        if (overflowRight > 1 || internalIsProblem || overflowLeft > 1) {
            results.push({
                tag: label(el),
                path: path(el),
                width: Math.round(rect.width),
                left: Math.round(rect.left),
                right: Math.round(rect.right),
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                overflowRight: Math.round(overflowRight),
                overflowLeft: Math.round(overflowLeft),
                internalOverflow: Math.round(internalOverflow),
                overflowX: overflowX,
                display: style.display,
                position: style.position,
                textPreview: (el.textContent || "").trim().slice(0, 80),
            });
        }
    }

    // Sort by "most overflowing" — prefer elements that overflow the viewport
    // and are leaf-ish (short path = high in tree = likely the cause)
    results.sort((a, b) => {
        const aScore = Math.max(a.overflowRight, a.internalOverflow, a.overflowLeft);
        const bScore = Math.max(b.overflowRight, b.internalOverflow, b.overflowLeft);
        return bScore - aScore;
    });

    return {
        viewportWidth: vw,
        documentScrollWidth: document.documentElement.scrollWidth,
        bodyScrollWidth: document.body.scrollWidth,
        overflowing: results.slice(0, 15),
    };
}
"""

# ── Page discovery ──────────────────────────────────────────────────────


def find_pages():
    pages = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(skip in rel.name for skip in SKIP_PATTERNS):
            continue
        if ".git" in p.parts:
            continue
        pages.append(p)
    return sorted(pages)


# ── Audit logic ─────────────────────────────────────────────────────────


async def audit_page(browser, page_path, target_width=TARGET_WIDTH):
    url = f"file://{page_path}"
    rel = page_path.relative_to(ROOT)

    # SOLA pages require auth — set sessionStorage before navigating
    context = await browser.new_context(viewport={"width": target_width, "height": TARGET_HEIGHT})
    page = await context.new_page()
    if "/sola/" in str(rel):
        await page.goto(f"file://{ROOT}/pages/research/overview/sola/sola-login.html", wait_until="domcontentloaded")
        await page.evaluate('sessionStorage.setItem("sola-auth", "verified")')

    try:
        await page.goto(url, wait_until="networkidle", timeout=15000)
    except Exception:
        # If networkidle times out (MathJax CDN), try domcontentloaded
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception as e:
            await context.close()
            return {"page": str(rel), "error": f"load failed: {e}"}

    # Wait for MathJax to finish rendering
    try:
        await page.wait_for_function(
            "() => { return window.MathJax && window.MathJax.startup && window.MathJax.startup.promise; }",
            timeout=3000,
        )
        await page.wait_for_function(
            "() => { if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) { return window.MathJax.startup.promise.then(() => true); } return true; }",
            timeout=SETTLE_TIMEOUT,
        )
    except Exception:
        pass  # No MathJax on this page, or timeout — proceed anyway

    # Extra settle time
    await page.wait_for_timeout(1000)

    # Run audit
    try:
        result = await page.evaluate(AUDIT_JS)
    except Exception as e:
        await context.close()
        return {"page": str(rel), "error": f"eval failed: {e}"}

    result["page"] = str(rel)
    await context.close()
    return result


async def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=TARGET_WIDTH)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    target_width = args.width

    pages = find_pages()
    print(f"Auditing {len(pages)} pages at {target_width}px viewport...\n", file=sys.stderr)

    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )

        for i, page_path in enumerate(pages):
            rel = page_path.relative_to(ROOT)
            r = await audit_page(browser, page_path, target_width)
            results.append(r)

            if "error" in r:
                status = "ERROR"
                detail = r["error"]
            elif r["documentScrollWidth"] > target_width + 2:
                status = "OVERFLOW"
                detail = f"doc scrollWidth={r['documentScrollWidth']}px (exceeds {target_width}px)"
            else:
                status = "OK"
                detail = f"doc scrollWidth={r['documentScrollWidth']}px"

            print(f"[{i+1}/{len(pages)}] {status:8s} {r['page']}", file=sys.stderr)
            if status != "OK" and args.verbose:
                print(f"           {detail}", file=sys.stderr)

        await browser.close()

    # ── Report ──────────────────────────────────────────────────────────

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable report
    ok = [r for r in results if "error" not in r and r.get("documentScrollWidth", 0) <= target_width + 2]
    bad = [r for r in results if "error" in r or r.get("documentScrollWidth", 0) > target_width + 2]

    print(f"\n{'='*70}")
    print(f"MOBILE AUDIT REPORT — target: {target_width}px viewport")
    print(f"{'='*70}")
    print(f"\nTotal pages: {len(results)}")
    print(f"OK:          {len(ok)}")
    print(f"Problems:    {len(bad)}")

    if bad:
        print(f"\n{'─'*70}")
        print("PAGES WITH OVERFLOW / ERRORS")
        print(f"{'─'*70}\n")

        for r in bad:
            page = r.get("page", "?")
            if "error" in r:
                print(f"  ERROR  {page}")
                print(f"         {r['error']}\n")
                continue

            doc_sw = r.get("documentScrollWidth", 0)
            excess = doc_sw - target_width
            print(f"  OVERFLOW  {page}")
            print(f"            document scrollWidth = {doc_sw}px ({excess}px over {target_width}px)")

            # Show top blocking elements
            for el in r.get("overflowing", [])[:3]:
                tag = el["tag"]
                path = el["path"]
                ow = el.get("overflowRight", 0)
                iw = el.get("internalOverflow", 0)
                ol = el.get("overflowLeft", 0)
                text = el.get("textPreview", "")

                parts = []
                if ow > 1:
                    parts.append(f"right+{ow}px")
                if iw > 1:
                    parts.append(f"internal+{iw}px")
                if ol > 1:
                    parts.append(f"left-{ol}px")

                print(f"            └─ {tag}  [{', '.join(parts)}]")
                print(f"               path: {path}")
                if text:
                    print(f"               text: \"{text}\"")
            print()

    # Summary table
    print(f"{'─'*70}")
    print("SUMMARY")
    print(f"{'─'*70}\n")
    print(f"{'Page':<55} {'Status':<8} {'DocSW':>6}")
    print(f"{'─'*55} {'─'*8} {'─'*6}")
    for r in results:
        page = r.get("page", "?")
        if "error" in r:
            status = "ERROR"
            sw = "-"
        elif r.get("documentScrollWidth", 0) > target_width + 2:
            status = "OVERFLOW"
            sw = str(r["documentScrollWidth"])
        else:
            status = "OK"
            sw = str(r.get("documentScrollWidth", "-"))
        print(f"{page:<55} {status:<8} {sw:>6}")


if __name__ == "__main__":
    asyncio.run(main())
