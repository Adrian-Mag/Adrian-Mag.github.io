# Plan: Add a shadow Codex host adapter to the Agent Ledger

**Status:** complete
**Created:** 2026-07-24

## Goal

Connect safe Codex lifecycle hooks to the private Agent Ledger without
interrupting work. Correlate a submitted prompt, subsequent host tool events,
and a later agent route declaration through one opaque work-phase token, while
retaining the existing control telemetry for comparison.

## Design decisions

- Codex hook events are evidence only when produced by the trusted host hook;
  the Agent Ledger records them with source `host`. Agent declarations remain
  source `agent`.
- `UserPromptSubmit` creates a pending opaque phase and records only the fact
  that a prompt arrived, never its text. `ledgerctl begin` claims that pending
  phase when the agent declares a workspace route. Tool events before the
  declaration remain correctly associated with it.
- An ordinary prompt with no workspace activity is not a violation. A pending
  phase is replaced on the next prompt if it has no observations. A pending
  phase with host activity but no route becomes a conservative missing-route
  finding.
- Concurrent hook handlers require an advisory runtime lock around event and
  state transactions. The lock protects ordinary local consistency, not against
  a process with filesystem write authority.
- The provider-specific adapter is tracked below `agent-ledger/adapters/codex/`;
  `.codex/config.toml` remains a thin local provider bridge. The existing
  `control` observer stays enabled in shadow mode and its historic data is not
  migrated.
- `Stop` is recorded as a turn stop. A true `SessionEnd` hook is used for a
  session end. Hosted tools outside Codex's local hook path remain unobserved.

## Phases

1. **Make the runtime hook-safe.** Add pending-phase correlation and locking;
   expand safe host event vocabulary and tests.
2. **Add the Codex adapter.** Add the thin safe-payload reducer, hook tests,
   and parallel local config entries while preserving legacy telemetry.
3. **Wire explanation and shadow exercise.** Update protocols, entry guidance,
   references, and public explorer; exercise a safe local hook payload and
   inspect only redacted runtime fields.
4. **Verify and settle.** Run focused tests, config syntax/static checks,
   privacy sweeps, search index, and completion records.

## Open questions

- What observation coverage does a real Codex run achieve over several normal
  tasks, especially for hosted and specialized tool paths?
- After a comparison period, which legacy control telemetry fields are still
  needed for continuity rather than Ledger observation?
