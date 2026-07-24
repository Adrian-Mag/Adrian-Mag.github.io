## Control telemetry and observation — Phase 2 complete
**Completed:** 2026-07-23

Registered local Codex lifecycle hooks for session start, prompt submission,
tool use, compaction, and stop. The observer retains only safe event categories
and is deliberately fail-open: it records possible gaps but cannot block work.
The canonical skill and maintenance guide now use `controlctl` at start,
classification, and close.

**Evidence:** synthetic Codex hook payload test; validator privacy checks;
manual inspection of the ignored `.codex/config.toml` registration.
