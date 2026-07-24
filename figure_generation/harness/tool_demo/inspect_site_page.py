#!/usr/bin/env python3
"""Read one public website page through a narrow, structured interface.

This is the real handler used by the Act 9 teaching exhibit. It reads one
repository-relative HTML file and reports page metadata, headings, and local
CSS/JavaScript dependencies. It does not return page prose or edit anything.

Input on stdin:  {"page": "pages/research/overview/harness/act-8.html"}
Output on stdout: {"ok": true, "result": {...}}
Errors:           {"ok": false, "error": {...}}
"""

from __future__ import annotations

import html
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


class PageParser(HTMLParser):
    """Collect the small page surface promised by the tool contract."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.description = ""
        self.headings: list[dict[str, Any]] = []
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self._capture: tuple[str, int] | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self._capture = (tag, 0)
            self._parts = []
        elif tag in ("h1", "h2", "h3"):
            self._capture = (tag, int(tag[1]))
            self._parts = []
        elif tag == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content") or ""
        elif tag == "link" and "stylesheet" in (values.get("rel") or "").split():
            href = values.get("href") or ""
            if href and not href.startswith(("http://", "https://", "//")):
                self.stylesheets.append(href)
        elif tag == "script":
            src = values.get("src") or ""
            if src and not src.startswith(("http://", "https://", "//")):
                self.scripts.append(src)

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self._capture or tag != self._capture[0]:
            return
        text = html.unescape(" ".join("".join(self._parts).split()))
        if tag == "title":
            self.title_parts.append(text)
        elif text:
            self.headings.append({"level": self._capture[1], "text": text})
        self._capture = None
        self._parts = []


class ToolInputError(ValueError):
    """A stable, user-correctable tool-input error."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def inspect_site_page(arguments: object) -> dict[str, Any]:
    """Validate the contract and return its promised structured result."""
    if not isinstance(arguments, dict) or set(arguments) != {"page"}:
        raise ToolInputError("invalid_arguments", "Expected one field named 'page'.")

    page = arguments.get("page")
    if not isinstance(page, str) or not page or Path(page).is_absolute():
        raise ToolInputError("invalid_page", "page must be a repository-relative path.")
    if Path(page).suffix.lower() != ".html":
        raise ToolInputError("invalid_page", "page must name an .html file.")

    candidate = (ROOT / page).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ToolInputError(
            "outside_repository", "page resolves outside the website repository."
        ) from exc
    if not candidate.is_file():
        raise ToolInputError("not_found", "page does not name an existing file.")

    parser = PageParser()
    parser.feed(candidate.read_text(encoding="utf-8"))
    return {
        "page": candidate.relative_to(ROOT).as_posix(),
        "title": " ".join(part for part in parser.title_parts if part),
        "description": parser.description,
        "headings": parser.headings,
        "stylesheets": parser.stylesheets,
        "scripts": parser.scripts,
    }


def main() -> int:
    try:
        arguments = json.load(sys.stdin)
        result = inspect_site_page(arguments)
    except json.JSONDecodeError:
        payload = {"ok": False, "error": {"code": "invalid_json", "message": "Input must be one JSON object."}}
    except ToolInputError as exc:
        payload = {"ok": False, "error": {"code": exc.code, "message": str(exc)}}
    except OSError as exc:
        payload = {"ok": False, "error": {"code": "read_failed", "message": str(exc)}}
    else:
        payload = {"ok": True, "result": result}

    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
