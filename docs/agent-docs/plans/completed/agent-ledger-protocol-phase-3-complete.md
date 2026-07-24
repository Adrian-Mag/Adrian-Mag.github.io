# Agent Ledger protocol — phase 3 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-protocol-plan.md`

## Landed

- Added the Agent Ledger entry to `AGENTS.md`, the cross-protocol map, the
  reference index, and the living agent-document and website references.
- Added the real folder and its public, plain-language explanation to the
  workspace explorer.
- Updated the Act 6 popup to remain a verbatim snapshot of `AGENTS.md`.

## Settled decision

`AGENTS.md` only directs an agent to the Agent Ledger when audit, procedure,
  reporting, or host-observation work is relevant. The ledger is not loaded as
  automatic task context.

## Verification

- Decoded Act 6 popup comparison matched `AGENTS.md` byte-for-byte.
- Workspace explorer inline JavaScript passed `node --check`.
- Both edited HTML documents parsed with Python's `HTMLParser`.
