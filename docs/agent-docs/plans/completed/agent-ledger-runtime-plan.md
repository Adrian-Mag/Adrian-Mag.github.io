# Plan: Implement the first Agent Ledger runtime

**Status:** complete
**Created:** 2026-07-24

## Goal

Turn the tracked Agent Ledger protocol into a small, private, local runtime:
a canonical standard-library command, an append-only event stream, a compact
current-state file, and a derived diagnostic report. Use it during this work,
but do not represent cooperative records as enforcement or tamper-proof audit.

## Design decisions

- `docs/agent-docs/agent-ledger/scripts/ledgerctl.py` is the sole supported
  writer for the Ledger runtime. It validates a deliberately small safe schema
  before atomically writing state or appending an event.
- `runtime/events.jsonl`, `runtime/state.json`, and `runtime/report.json` are
  ignored, local-only files. They contain opaque work-phase tokens and controlled
  categories, never prompts, commands, raw paths, content, outputs, or logs.
- `begin`, `reclassify`, `record`, `observe`, `check`, `close`, and `report`
  cover the initial declared/observed workflow. `observe` is meaningful only
  when called by a host adapter; the command itself cannot make an agent's
  self-report independent.
- The first reporter identifies only evidence gaps that the data supports,
  such as a missing declared route or an unclosed phase. It does not invent a
  route/action mismatch rule from a vague tool event.
- Tests use temporary runtime folders. No provider hook, daemon, migration, or
  enforcement gate is part of this phase.

## Phases

1. **Specify the executable boundary.** Extend the tracked protocol/schema for
   runtime filenames, controlled state fields, and command ownership.
2. **Implement the runtime.** Add `ledgerctl.py` and focused stdlib tests for
   valid writes, rejected unsafe input, state transitions, and reports.
3. **Wire discovery and demonstrate use.** Update entry/reference/public
   explanations and use the Ledger for this planned work phase.
4. **Verify and settle.** Run the focused tests, inspect only safe generated
   runtime fields, rebuild search index after prose changes, and archive phase
   records.

## Open questions

- Which provider-facing hook surfaces can call `observe` independently of the
  agent, and how should their trust boundary be described?
- Should a future reporter compare particular routes with Git events, and only
  after a human-approved rule specifies the valid relationship?
