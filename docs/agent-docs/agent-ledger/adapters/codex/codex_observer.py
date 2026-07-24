#!/usr/bin/env python3
"""Shadow-mode Codex hook adapter for safe Agent Ledger observations.

The hook payload can contain prompts, transcript paths, tool arguments, and
other private values. This adapter deliberately reads only the event name, cwd,
and controlled tool name; it passes no raw provider value into the Ledger.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import ledgerctl  # noqa: E402  # Canonical local writer lives beside the protocol.


def repository(cwd: str | None) -> Path:
    """Resolve the hook's repository without retaining the raw cwd in an event."""
    return Path(subprocess.run(["git", "-C", cwd or str(Path.cwd()), "rev-parse", "--show-toplevel"], check=True, text=True, capture_output=True).stdout.strip())


def tool_class(name: str) -> str:
    """Reduce a provider tool name to the Ledger's controlled action class."""
    if name in {"apply_patch", "Edit", "Write"}:
        return "patch"
    if name in {"Bash", "exec_command"}:
        return "shell"
    if name.startswith("mcp__"):
        return "mcp"
    return "local_function" if name else "other"


def observe(payload: dict[str, object]) -> None:
    """Map one Codex hook event into safe pending/open-phase observations."""
    repo = repository(payload.get("cwd") if isinstance(payload.get("cwd"), str) else None)
    runtime = ledgerctl.default_runtime(repo)
    name = str(payload.get("hook_event_name", ""))
    if name == "UserPromptSubmit":
        ledgerctl.begin_turn(runtime)
    elif name == "SessionStart":
        ledgerctl.observe_host(runtime, "host.session_started")
    elif name == "PreToolUse":
        ledgerctl.observe_host(runtime, "host.tool_requested", tool_class(str(payload.get("tool_name", ""))))
    elif name == "PostToolUse":
        ledgerctl.observe_host(runtime, "host.tool_completed", tool_class(str(payload.get("tool_name", ""))))
    elif name == "PreCompact":
        ledgerctl.observe_host(runtime, "host.context_pre_compact")
    elif name == "PostCompact":
        ledgerctl.observe_host(runtime, "host.context_post_compact")
    elif name == "Stop":
        ledgerctl.observe_host(runtime, "host.turn_stopped")
    elif name == "SessionEnd":
        ledgerctl.observe_host(runtime, "host.session_ended")


def main() -> int:
    """Keep shadow observation non-blocking if a local hook ever fails."""
    try:
        payload = json.load(sys.stdin)
        if isinstance(payload, dict):
            observe(payload)
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
