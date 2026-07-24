# Agent Ledger protocol — phase 1 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-protocol-plan.md`

## Landed

- Added `docs/agent-docs/agent-ledger/PROTOCOL.md` as the tracked ownership,
  privacy, runtime, and non-enforcement contract.
- Reserved `runtime/` as ignored local state; added the matching `.gitignore`
  rule.

## Settled decision

The Agent Ledger is a soft observation protocol, not a router, permission
system, skill, hook, or claim of tamper-proof logging. The existing ignored
`control/` telemetry remains live legacy machinery.

## Verification

- Confirmed the runtime directory exists and is ignored by Git.
