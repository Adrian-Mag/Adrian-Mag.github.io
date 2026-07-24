#!/usr/bin/env python3
"""Codex PreToolUse demo: guard one generated website asset.

Threat model: reduce accidental direct changes to the generated search index.
This is deliberately a small string blocklist, not a security boundary. It
blocks every Bash command that contains the protected path unless the command
is the one approved rebuild command. That makes its false positives and its
easy string-construction bypass visible enough to teach from.
"""

from __future__ import annotations

import json
import sys


PROTECTED_PATH = "media/search-index.json"
APPROVED_REBUILD = "python3 tools/build_search_index.py"
DENIAL_REASON = (
    "Direct access to media/search-index.json is blocked. "
    "Regenerate it with python3 tools/build_search_index.py."
)


def verdict(payload: object) -> dict[str, object] | None:
    """Return a Codex denial object, or ``None`` to allow the event."""
    if not isinstance(payload, dict):
        return None
    if payload.get("hook_event_name") != "PreToolUse":
        return None
    if payload.get("tool_name") != "Bash":
        return None

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    command = tool_input.get("command")
    if not isinstance(command, str):
        return None

    if command.strip() == APPROVED_REBUILD:
        return None
    if PROTECTED_PATH not in command:
        return None

    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENIAL_REASON,
        }
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0

    decision = verdict(payload)
    if decision is not None:
        json.dump(decision, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
