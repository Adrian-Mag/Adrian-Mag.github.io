#!/usr/bin/env python3
"""
Extract real tool-loop traces for Act 4 of "The Machine Around the Model".

Reads Claude Code session logs from ~/.claude/projects/ and emits the
model-asks / harness-answers alternation as JSON for the Act 4 panel.

WHY THESE SESSIONS
------------------
Both traces are taken from sessions in the *website* repository, which is
public by construction. Sessions from every other workspace are deliberately
excluded.

ELISION POLICY
--------------
Tool results can be enormous (base64 screenshots, whole-file reads). They are
truncated here, but every truncation is marked `"elided": true` and carries
the original length, and the panel renders that visibly. A trace that silently
dropped steps would be a tidied-up exhibit, which is exactly what this series
claims not to publish.

Output: media/research/harness/toolloop.json
Run:    python3 figure_generation/harness/extract_toolloop.py
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "media" / "research" / "harness" / "toolloop.json"
SESSIONS = Path.home() / ".claude" / "projects" / "-home-adrian-PhD-Adrian-Mag-github-io"

MAX_TEXT = 240          # characters kept from any single field
SECRET_RE = re.compile(
    r"([0-9]{1,3}\.){3}[0-9]{1,3}|sk-ant-[A-Za-z0-9_-]{6,}|ghp_[A-Za-z0-9]{6,}"
)


def clip(s: str) -> tuple[str, bool, int]:
    """Collapse whitespace and truncate, reporting whether truncation happened."""
    flat = " ".join((s or "").split())
    if len(flat) <= MAX_TEXT:
        return flat, False, len(flat)
    return flat[:MAX_TEXT].rstrip(), True, len(flat)


def text_of(c) -> str:
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(text_of(x) for x in c)
    if isinstance(c, dict):
        return text_of(c.get("content") or c.get("text") or "")
    return ""


def describe_input(inp: dict) -> str:
    """
    A readable one-liner for a tool call.

    Tools differ in where the interesting argument lives — Bash uses `command`,
    Read uses `file_path`, MCP tools use `code`, `url`, `selector`, and so on.
    Falling back to an empty string (as an earlier version did) produced blank
    rows in the exhibit, which reads as 'nothing happened' rather than 'we did
    not look in the right field'.
    """
    for k in ("command", "file_path", "pattern", "query", "url", "code",
              "filename", "selector", "element", "text"):
        v = inp.get(k)
        if isinstance(v, str) and v.strip():
            return v
    keys = [k for k in inp.keys() if not k.startswith("_")]
    return "(" + ", ".join(keys) + ")" if keys else "(no arguments)"


def describe_result(c: dict) -> tuple[str, bool]:
    """
    Return (text, is_non_text). Tool results are not always text: an image read
    returns image blocks, which text_of() flattens to "". Label those explicitly
    rather than emitting an empty step.
    """
    body = c.get("content")
    blocks = body if isinstance(body, list) else []
    kinds = {b.get("type") for b in blocks if isinstance(b, dict)}
    t = text_of(c)
    if not t.strip() and kinds:
        non_text = ", ".join(sorted(k for k in kinds if k and k != "text"))
        return f"[{non_text or 'non-text'} content returned to the model]", True
    if not t.strip():
        return "[empty result]", True
    return t, False


def load(fp: Path) -> list[dict]:
    recs = []
    with fp.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:                      # no size filter — see module docstring
            try:
                recs.append(json.loads(line))
            except Exception:
                pass
    return recs


def steps_from(recs: list[dict], start_ts: str, end_ts: str) -> list[dict]:
    """Flatten a time window into an ordered model/harness alternation."""
    out = []
    for r in recs:
        ts = (r.get("timestamp") or "")
        if not (start_ts <= ts <= end_ts):
            continue
        msg = r.get("message") or {}
        cont = msg.get("content")
        if not isinstance(cont, list):
            continue
        for c in cont:
            if not isinstance(c, dict):
                continue
            kind = c.get("type")
            if kind == "text" and msg.get("role") == "assistant":
                t, cut, n = clip(text_of(c))
                if t:
                    out.append({"actor": "model", "kind": "say", "text": t,
                                "elided": cut, "full_len": n, "at": ts[11:19]})
            elif kind == "tool_use":
                t, cut, n = clip(describe_input(c.get("input") or {}))
                out.append({"actor": "model", "kind": "request", "tool": c.get("name"),
                            "text": t, "elided": cut, "full_len": n, "at": ts[11:19]})
            elif kind == "tool_result":
                raw, non_text = describe_result(c)
                t, cut, n = clip(raw)
                out.append({"actor": "harness", "kind": "result", "text": t,
                            "elided": cut, "full_len": n, "non_text": non_text,
                            "at": ts[11:19]})
    return out


TRACES = [
    {
        "id": "minimal",
        "file": "5288737a-ecb1-410d-87f5-4bf2628fec90.jsonl",
        "window": ("2026-07-16T16:44:15", "2026-07-16T16:44:25"),
        "label": "The whole mechanism, in three steps",
        "note": "The model did not run pwd. It asked; the harness ran it and appended "
                "the answer; the model then read that answer and spoke.",
    },
    {
        "id": "iterating",
        "file": "6f674b3c-8a3a-4ae2-888a-bc089c5baef4.jsonl",
        "window": ("2026-07-18T12:18:20", "2026-07-18T12:19:05"),
        "label": "The loop, iterating",
        "note": "Looking at a web page: the model cannot see one. It asks for a scroll, "
                "asks for a screenshot, then asks to read the resulting file — three "
                "round trips for what a person does with one glance.",
    },
]


def main() -> None:
    traces = []
    for spec in TRACES:
        fp = SESSIONS / spec["file"]
        if not fp.exists():
            print(f"  skip {spec['id']}: {fp.name} not found")
            continue
        steps = steps_from(load(fp), *spec["window"])
        if not steps:
            print(f"  skip {spec['id']}: no steps in window")
            continue
        traces.append({
            "id": spec["id"], "label": spec["label"], "note": spec["note"],
            "source": f"~/.claude/projects/.../{spec['file'][:8]}….jsonl",
            "steps": steps,
        })
        cut = sum(1 for s in steps if s["elided"])
        print(f"  {spec['id']}: {len(steps)} steps ({cut} truncated)")

    payload = {
        "_comment": ("Extracted verbatim from real Claude Code session logs by "
                     "figure_generation/harness/extract_toolloop.py. Long tool results are "
                     "truncated, and every truncation is flagged 'elided' and shown as such "
                     "in the panel. No step is silently dropped."),
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "traces": traces,
    }

    blob = json.dumps(payload, indent=2, ensure_ascii=False)
    leaks = [m.group(0) for m in SECRET_RE.finditer(blob)
             if m.group(0) not in ("0.0.0.0", "127.0.0.1")]
    if leaks:
        raise SystemExit(f"ABORT — possible sensitive strings in output: {set(leaks)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(blob + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(traces)} traces)")


if __name__ == "__main__":
    main()
