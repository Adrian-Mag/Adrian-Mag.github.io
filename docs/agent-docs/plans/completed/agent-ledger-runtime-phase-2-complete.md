# Agent Ledger runtime — phase 2 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-runtime-plan.md`

## Landed

- Added `scripts/ledgerctl.py` for declared route, reclassification, record,
  procedure-step, check, host/Git observation, close, state, and report actions.
- Added focused standard-library tests covering a closed phase, an unclosed
  diagnostic finding, and rejected unsafe work-phase input.

## Settled decision

`observe` is only independently meaningful when a real host or Git adapter
calls it. The command itself cannot turn an agent's statement into independent
evidence.

## Verification

- Focused runtime tests passed.
- Python byte-compilation passed.
