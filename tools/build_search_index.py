#!/usr/bin/env python3
"""
Build the client-side search index for the site.

Walks the notes series (and a few key standalone pages), extracts each
page's title, description, and visible text (tags stripped, LaTeX source
kept as-is so formula names like "trace-class" remain findable), and
writes a single JSON file the search page fetches on demand.

Run after editing any notes page:

    python3 tools/build_search_index.py

Output: media/search-index.json
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "search-index.json"

# Directories whose every page is indexed, plus standalone extras.
SERIES_DIRS = [
    ("pages/research/overview/sola", "My Take on SOLA"),
    ("pages/research/overview/think-first", "Think First, Discretize Later"),
    ("pages/research/overview/bayes", "Bayes, Measure-Theoretically"),
    ("pages/research/overview/frequentist", "Bayesian vs Frequentist"),
    ("pages/research/overview/cg", "The Road to Conjugate Gradients"),
    ("pages/research/overview/harness", "The Machine Around the Model"),
]
EXTRA_PAGES = [
    ("pages/research/overview/index.html", None),
    ("pages/research/overview/ai-in-practice.html", None),
    ("pages/research/overview/inversions-inferences.html", None),
    ("pages/research/publications/papers.html", None),
    ("pages/research/posters/posters.html", None),
    ("pages/about.html", None),
]
SKIP_NAMES = {"part-3.html"}  # redirect tombstones


class TextExtractor(HTMLParser):
    """Collects visible text from <main>, skipping script/style/svg."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.chunks: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
        elif tag == "title":
            self._in_title = True
        elif tag in ("script", "style", "svg", "noscript"):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        elif tag == "title":
            self._in_title = False
        elif tag in ("script", "style", "svg", "noscript"):
            self.skip_depth = max(0, self.skip_depth - 1)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.in_main and self.skip_depth == 0:
            self.chunks.append(data)


def extract(path: Path) -> dict | None:
    html = path.read_text(encoding="utf-8")

    parser = TextExtractor()
    parser.feed(html)
    text = re.sub(r"\s+", " ", " ".join(parser.chunks)).strip()
    if not text:
        return None

    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.S)
    desc = m.group(1).strip() if m else ""

    return {
        "url": "/" + path.relative_to(ROOT).as_posix(),
        "title": parser.title.strip() or path.stem,
        "desc": desc,
        "text": text,
    }


def main() -> None:
    entries = []

    for rel_dir, series in SERIES_DIRS:
        for path in sorted((ROOT / rel_dir).glob("*.html")):
            if path.name in SKIP_NAMES:
                continue
            entry = extract(path)
            if entry:
                entry["series"] = series
                entries.append(entry)

    for rel, series in EXTRA_PAGES:
        path = ROOT / rel
        if path.exists():
            entry = extract(path)
            if entry:
                if series:
                    entry["series"] = series
                entries.append(entry)

    OUT.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    total_kb = OUT.stat().st_size / 1024
    print(f"indexed {len(entries)} pages -> {OUT.relative_to(ROOT)} ({total_kb:.0f} KB)")


if __name__ == "__main__":
    main()
