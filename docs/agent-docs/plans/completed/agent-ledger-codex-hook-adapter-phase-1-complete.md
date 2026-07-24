# Agent Ledger Codex hook adapter — phase 1 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-codex-hook-adapter-plan.md`

## Landed

- Added a pending opaque phase on a safe host prompt-submission event.
- `ledgerctl begin` now claims that phase, so later route evidence and earlier
  supported host-tool observations share one token.
- Added advisory locking around Ledger event/state transactions and expanded
  the safe host-event and coarse tool-class vocabulary.

## Verification

- Focused tests include twelve concurrent hook-style writers without lost
  records, plus a pending-phase correlation test.
