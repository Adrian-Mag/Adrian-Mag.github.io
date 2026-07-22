## Plan: Compact control-record retention
**Status:** completed   **Created:** 2026-07-22   **Completed:** 2026-07-22

### Goal

Make the agent-docs records easy to resume from without turning local control
files into a project diary. Keep current constraints and next actions close at
hand, while preserving durable decisions and evidence in tracked records.

### Design notes

- `HANDOFF.json` is one replaceable local snapshot, not an archive.
- `CURRENT.md` is compact workspace orientation, not session history.
- An active plan holds decisions that still constrain unfinished work.
- A phase-completion record preserves resolved decisions, deviations, and
  verification evidence when that phase lands.
- Living references hold current architecture; source dossiers hold claim and
  artifact provenance. Neither becomes a general decision log.

### Files / components

- `docs/agent-docs/PROTOCOL.md`
- `docs/agent-docs/control/skills/website-control/SKILL.md`
- `docs/agent-docs/control/MAINTENANCE.md`
- `docs/agent-docs/control/CURRENT.md` and `HANDOFF.json` (local-only)

### Phases

1. **Implement and validate retention roles.** **Completed.** The protocol and
   local workflow now assign each record a distinct role; the local current and
   handoff notes were replaced with concise snapshots.

### Closing note

The work matched the approved design. No historical handoff archive was kept:
durable decisions and evidence remain in tracked plans and phase-completion
records, while local control retains only current state.
