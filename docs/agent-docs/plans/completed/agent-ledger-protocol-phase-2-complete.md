# Agent Ledger protocol — phase 2 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-protocol-plan.md`

## Landed

- Added `EVENT_SCHEMA.md` with separate declared, observed, and derived event
  vocabulary plus a privacy-safe common field set.
- Added `PROCEDURES.md` and `REPORTING.md` with an honest default work sequence
  and gap-report semantics.

## Settled decision

Missing evidence is a diagnostic gap, not proof of misconduct. Neither an
agent declaration nor a host observation proves that a document was understood
or a decision was correct.

## Verification

- Read the protocol documents together to confirm they make no runtime,
  adapter, gate, or anti-tamper claim that the workspace cannot support.
