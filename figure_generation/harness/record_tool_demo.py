#!/usr/bin/env python3
"""Record real calls to the Act 9 website-local tool handler.

The recorder invokes the exact public handler in a subprocess. It records one
successful inspection and one rejected traversal attempt. The rejection is an
input-validation probe; no path outside the repository is read.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HANDLER = ROOT / "figure_generation" / "harness" / "tool_demo" / "inspect_site_page.py"
OUT = ROOT / "media" / "research" / "harness" / "tool-demo.json"

CASES = [
    {
        "id": "inspect-act-8",
        "label": "Allowed page inspection",
        "arguments": {"page": "pages/research/overview/harness/act-8.html"},
    },
    {
        "id": "reject-traversal",
        "label": "Rejected path traversal",
        "arguments": {"page": "../outside.html"},
    },
]


def run_case(case: dict[str, object]) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(HANDLER)],
        cwd=ROOT,
        input=json.dumps(case["arguments"]),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stderr:
        raise RuntimeError(f"handler wrote to stderr: {completed.stderr.strip()}")
    return {
        **case,
        "exit_code": completed.returncode,
        "response": json.loads(completed.stdout),
    }


def main() -> None:
    payload = {
        "_comment": (
            "Recorded by invoking the public inspect_site_page.py handler. "
            "The traversal case was rejected before any outside path was read."
        ),
        "recorded_on": date.today().isoformat(),
        "tool_definition": "figure_generation/harness/tool_demo/tool.json",
        "handler": "figure_generation/harness/tool_demo/inspect_site_page.py",
        "cases": [run_case(case) for case in CASES],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(CASES)} recorded calls)")


if __name__ == "__main__":
    main()
