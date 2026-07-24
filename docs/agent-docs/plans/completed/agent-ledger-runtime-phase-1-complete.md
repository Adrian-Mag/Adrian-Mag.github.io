# Agent Ledger runtime — phase 1 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-runtime-plan.md`

## Landed

- Specified the three ignored runtime files: `events.jsonl`, `state.json`, and
  `report.json`.
- Extended the schema with controlled record and procedure-step categories plus
  opaque work-phase-token rules.

## Settled decision

The runtime can make normal local writes durable and repeatable, but it is not
append-only in a strong security sense and must not be described as tamper-proof.
