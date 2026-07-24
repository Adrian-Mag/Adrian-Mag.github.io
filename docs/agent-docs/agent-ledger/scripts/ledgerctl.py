#!/usr/bin/env python3
"""Private, schema-checked runtime for the Agent Ledger protocol.

The Ledger is diagnostic evidence, not an authority or an audit guarantee.
This command deliberately accepts only controlled categories and opaque work
phase identifiers. It rejects prompts, commands, paths, content, output, and
other transcript-like data rather than attempting to redact it after writing.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised only on non-POSIX hosts.
    fcntl = None  # type: ignore[assignment]


SCHEMA_VERSION = 1
ROUTES = {"conversation", "research", "inspect", "plan", "change-small", "change-planned", "external", "uncertain"}
RECORD_TYPES = {"plan", "reference", "source", "other"}
STEPS = {"work", "plan-updated", "reference-updated"}
OUTCOMES = {"observed", "passed", "failed", "missing"}
TOOL_CLASSES = {"shell", "patch", "mcp", "local_function", "other"}
HOST_EVENTS = {"host.turn_submitted", "host.session_started", "host.tool_requested", "host.tool_completed", "host.context_pre_compact", "host.context_post_compact", "host.turn_stopped", "host.session_ended", "git.commit_attempted", "git.commit_completed"}
AGENT_EVENTS = {"agent.route_declared", "agent.route_reclassified", "agent.record_selected", "agent.procedure_step_declared", "agent.check_declared", "agent.work_closed"}
WORK_PHASE = re.compile(r"^wp-[0-9a-f]{24}$")


def utc_now() -> str:
    """Return a compact UTC timestamp for an event or state transition."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def default_runtime(repo: Path) -> Path:
    """Locate the ignored Ledger runtime below a repository root."""
    return repo / "docs" / "agent-docs" / "agent-ledger" / "runtime"


def paths(runtime: Path) -> dict[str, Path]:
    """Return the three local runtime files without exposing project content."""
    return {"events": runtime / "events.jsonl", "state": runtime / "state.json", "report": runtime / "report.json", "lock": runtime / ".ledger.lock"}


@contextmanager
def runtime_lock(runtime: Path):
    """Serialize local state/event transactions; this is not a security boundary."""
    target = paths(runtime)["lock"]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a+", encoding="utf-8") as handle:
        if fcntl is None:
            raise OSError("Agent Ledger hook runtime requires a POSIX advisory lock")
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def initial_state() -> dict[str, Any]:
    """Return the safe initial state for a runtime with no active work phase."""
    return {"schema_version": SCHEMA_VERSION, "visibility": "local-only", "status": "idle"}


def load_json(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    """Load an object-valued JSON record, or use the provided first-run value."""
    if not path.exists():
        return fallback
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def save_json(path: Path, value: dict[str, Any]) -> None:
    """Atomically replace a small runtime JSON record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_events(path: Path) -> list[dict[str, Any]]:
    """Read the local newline-delimited event stream and validate its shape."""
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError(f"events.jsonl line {number} must be an object")
        validate_event(event)
        events.append(event)
    return events


def validate_phase(value: str) -> str:
    """Accept only an opaque generated work-phase token."""
    if not WORK_PHASE.fullmatch(value):
        raise ValueError("work phase must be an opaque token in the form wp-<24 lowercase hex characters>")
    return value


def validate_event(event: dict[str, Any]) -> None:
    """Reject unknown fields and values before an event is trusted or reported."""
    allowed = {"schema_version", "at", "kind", "work_phase", "route", "source", "outcome", "record_type", "step", "tool_class"}
    unknown = set(event) - allowed
    if unknown:
        raise ValueError("event contains unsupported fields: " + ", ".join(sorted(unknown)))
    required = {"schema_version", "at", "kind", "work_phase", "source", "outcome"}
    missing = required - set(event)
    if missing:
        raise ValueError("event lacks required fields: " + ", ".join(sorted(missing)))
    if event["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported event schema version")
    if event["kind"] not in AGENT_EVENTS | HOST_EVENTS:
        raise ValueError("unknown event kind")
    validate_phase(str(event["work_phase"]))
    if event["source"] not in {"agent", "host", "git"}:
        raise ValueError("unknown event source")
    if event["outcome"] not in OUTCOMES:
        raise ValueError("unknown event outcome")
    if "route" in event and event["route"] not in ROUTES:
        raise ValueError("unknown route")
    if "record_type" in event and event["record_type"] not in RECORD_TYPES:
        raise ValueError("unknown record type")
    if "step" in event and event["step"] not in STEPS:
        raise ValueError("unknown procedure step")
    if "tool_class" in event and event["tool_class"] not in TOOL_CLASSES:
        raise ValueError("unknown tool class")


def append_event_unlocked(runtime: Path, event: dict[str, Any]) -> None:
    """Append one validated event while the caller holds the runtime lock."""
    validate_event(event)
    target = paths(runtime)["events"]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def append_event(runtime: Path, item: dict[str, Any]) -> None:
    """Append one event under the local advisory lock; it is not tamper-proof."""
    with runtime_lock(runtime):
        append_event_unlocked(runtime, item)


def current_phase(state: dict[str, Any], supplied: str | None) -> str:
    """Use an explicit safe phase or the one currently open in local state."""
    if supplied:
        return validate_phase(supplied)
    phase = state.get("work_phase")
    if not isinstance(phase, str):
        raise ValueError("no active work phase; start one with begin")
    return validate_phase(phase)


def event(kind: str, phase: str, source: str, outcome: str = "observed", **extra: str) -> dict[str, Any]:
    """Build a schema-checked event using only controlled metadata."""
    item: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "at": utc_now(), "kind": kind, "work_phase": phase, "source": source, "outcome": outcome}
    item.update(extra)
    validate_event(item)
    return item


def open_state(phase: str, route: str) -> dict[str, Any]:
    """Create compact current state without copying task text or file names."""
    now = utc_now()
    return {"schema_version": SCHEMA_VERSION, "visibility": "local-only", "status": "open", "work_phase": phase, "route": route, "opened_at": now, "updated_at": now, "selected_record_types": [], "declared_steps": [], "checks": []}


def require_open(state: dict[str, Any]) -> None:
    """Keep agent-declared lifecycle operations within one open work phase."""
    if state.get("status") != "open":
        raise ValueError("an open work phase is required; start one with begin")


def begin(runtime: Path, route: str) -> int:
    """Open a work phase, declare its route, and write its opaque state token."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        if state.get("status") == "open":
            raise ValueError("a work phase is already open; close it or reclassify it first")
        phase = state["work_phase"] if state.get("status") == "pending" else "wp-" + uuid.uuid4().hex[:24]
        validate_phase(phase)
        append_event_unlocked(runtime, event("agent.route_declared", phase, "agent", route=route))
        save_json(target, open_state(phase, route))
    print(phase)
    return 0


def reclassify(runtime: Path, route: str, supplied_phase: str | None) -> int:
    """Declare a new controlled route for the current open work phase."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        require_open(state)
        phase = current_phase(state, supplied_phase)
        append_event_unlocked(runtime, event("agent.route_reclassified", phase, "agent", route=route))
        state["route"] = route
        state["updated_at"] = utc_now()
        save_json(target, state)
    return 0


def record(runtime: Path, record_type: str, supplied_phase: str | None) -> int:
    """Declare selection of a record category without recording its path or contents."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        require_open(state)
        phase = current_phase(state, supplied_phase)
        append_event_unlocked(runtime, event("agent.record_selected", phase, "agent", record_type=record_type))
        selected = state.setdefault("selected_record_types", [])
        if record_type not in selected:
            selected.append(record_type)
        state["updated_at"] = utc_now()
        save_json(target, state)
    return 0


def declare_step(runtime: Path, step: str, supplied_phase: str | None) -> int:
    """Declare a controlled procedure step without recording hidden reasoning."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        require_open(state)
        phase = current_phase(state, supplied_phase)
        append_event_unlocked(runtime, event("agent.procedure_step_declared", phase, "agent", step=step))
        declared = state.setdefault("declared_steps", [])
        if step not in declared:
            declared.append(step)
        state["updated_at"] = utc_now()
        save_json(target, state)
    return 0


def check(runtime: Path, outcome: str, supplied_phase: str | None) -> int:
    """Declare that a check ran and record only its controlled result category."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        require_open(state)
        phase = current_phase(state, supplied_phase)
        append_event_unlocked(runtime, event("agent.check_declared", phase, "agent", outcome=outcome))
        state.setdefault("checks", []).append(outcome)
        state["updated_at"] = utc_now()
        save_json(target, state)
    return 0


def observe(runtime: Path, kind: str, supplied_phase: str | None) -> int:
    """Record a host/Git event; callers must supply the independent adapter boundary."""
    with runtime_lock(runtime):
        state = load_json(paths(runtime)["state"], initial_state())
        phase = current_phase(state, supplied_phase)
        source = "git" if kind.startswith("git.") else "host"
        append_event_unlocked(runtime, event(kind, phase, source))
    return 0


def begin_turn(runtime: Path) -> str:
    """Start an opaque pending phase from a host prompt event without its text."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        phase = state.get("work_phase") if state.get("status") == "open" else "wp-" + uuid.uuid4().hex[:24]
        validate_phase(str(phase))
        if state.get("status") != "open":
            state = {"schema_version": SCHEMA_VERSION, "visibility": "local-only", "status": "pending", "work_phase": phase, "pending_at": utc_now(), "updated_at": utc_now()}
            save_json(target, state)
        append_event_unlocked(runtime, event("host.turn_submitted", str(phase), "host"))
        return str(phase)


def observe_host(runtime: Path, kind: str, tool_class: str | None = None) -> bool:
    """Append a safe hook observation only while a pending/open phase exists."""
    with runtime_lock(runtime):
        state = load_json(paths(runtime)["state"], initial_state())
        if state.get("status") not in {"pending", "open"}:
            return False
        phase = current_phase(state, None)
        extra = {"tool_class": tool_class} if tool_class else {}
        append_event_unlocked(runtime, event(kind, phase, "host", **extra))
        return True


def close(runtime: Path, supplied_phase: str | None) -> int:
    """Close the active phase and retain only safe compact state for inspection."""
    target = paths(runtime)["state"]
    with runtime_lock(runtime):
        state = load_json(target, initial_state())
        require_open(state)
        phase = current_phase(state, supplied_phase)
        append_event_unlocked(runtime, event("agent.work_closed", phase, "agent", outcome="passed"))
        state["status"] = "closed"
        state["closed_at"] = utc_now()
        state["updated_at"] = state["closed_at"]
        save_json(target, state)
    return 0


def findings(events: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive only conservative evidence gaps from the safe event stream."""
    by_phase: dict[str, list[dict[str, Any]]] = {}
    for item in events:
        by_phase.setdefault(item["work_phase"], []).append(item)
    result: list[dict[str, Any]] = []
    for phase, phase_events in sorted(by_phase.items()):
        kinds = {item["kind"] for item in phase_events}
        host_activity = bool(kinds & {"host.tool_requested", "host.tool_completed", "git.commit_attempted", "git.commit_completed"})
        if host_activity and "agent.route_declared" not in kinds:
            result.append({"schema_version": SCHEMA_VERSION, "kind": "ledger.expected_evidence_missing", "work_phase": phase, "source": "derived", "outcome": "missing", "expected": "agent.route_declared"})
    if state.get("status") == "open" and isinstance(state.get("work_phase"), str):
        result.append({"schema_version": SCHEMA_VERSION, "kind": "ledger.work_phase_unclosed", "work_phase": state["work_phase"], "source": "derived", "outcome": "missing", "expected": "agent.work_closed"})
    return result


def report(runtime: Path) -> int:
    """Write and print a derived diagnostic report without appending synthetic events."""
    target = paths(runtime)
    with runtime_lock(runtime):
        state = load_json(target["state"], initial_state())
        events = load_events(target["events"])
        value = {"schema_version": SCHEMA_VERSION, "visibility": "local-only", "generated_at": utc_now(), "event_count": len(events), "state_status": state.get("status", "unknown"), "findings": findings(events, state)}
        save_json(target["report"], value)
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


def status(runtime: Path) -> int:
    """Print the compact current state; it is orientation, not a history."""
    print(json.dumps(load_json(paths(runtime)["state"], initial_state()), indent=2, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    """Build the narrow command-line interface for safe Ledger operations."""
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--repo", type=Path, default=Path.cwd())
    root.add_argument("--runtime", type=Path, help="override ignored runtime directory; intended for focused tests")
    commands = root.add_subparsers(dest="command", required=True)
    begin_parser = commands.add_parser("begin", help="open a work phase and declare its route")
    begin_parser.add_argument("--route", required=True, choices=sorted(ROUTES))
    reclassify_parser = commands.add_parser("reclassify", help="declare a new route for the open phase")
    reclassify_parser.add_argument("--route", required=True, choices=sorted(ROUTES))
    record_parser = commands.add_parser("record", help="declare a selected record category")
    record_parser.add_argument("--record-type", required=True, choices=sorted(RECORD_TYPES))
    step_parser = commands.add_parser("step", help="declare a controlled procedure step")
    step_parser.add_argument("--step", required=True, choices=sorted(STEPS))
    check_parser = commands.add_parser("check", help="declare a check result category")
    check_parser.add_argument("--outcome", default="passed", choices=sorted(OUTCOMES))
    observe_parser = commands.add_parser("observe", help="record a host/Git event from an adapter")
    observe_parser.add_argument("--kind", required=True, choices=sorted(HOST_EVENTS))
    commands.add_parser("close", help="close the active phase")
    commands.add_parser("report", help="write a diagnostic report")
    commands.add_parser("status", help="print compact current state")
    for name in ("reclassify", "record", "step", "check", "observe", "close"):
        commands.choices[name].add_argument("--work-phase")
    return root


def main() -> int:
    """Dispatch one schema-checked Ledger operation and report safe failures."""
    args = parser().parse_args()
    runtime = args.runtime or default_runtime(args.repo.resolve())
    try:
        if args.command == "begin":
            return begin(runtime, args.route)
        if args.command == "reclassify":
            return reclassify(runtime, args.route, args.work_phase)
        if args.command == "record":
            return record(runtime, args.record_type, args.work_phase)
        if args.command == "step":
            return declare_step(runtime, args.step, args.work_phase)
        if args.command == "check":
            return check(runtime, args.outcome, args.work_phase)
        if args.command == "observe":
            return observe(runtime, args.kind, args.work_phase)
        if args.command == "close":
            return close(runtime, args.work_phase)
        if args.command == "report":
            return report(runtime)
        return status(runtime)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
