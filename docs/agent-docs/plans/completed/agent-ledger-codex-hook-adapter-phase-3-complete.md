# Agent Ledger Codex hook adapter — phase 3 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-codex-hook-adapter-plan.md`

## Landed

- Updated the Ledger protocol, schema, reporting rules, AGENTS guidance,
  living reference, source dossier, Act 6 snapshot, and public explorer.
- Ran a safe synthetic Codex hook payload through the real adapter, then had
  `ledgerctl begin` claim its pending phase and verified the safe correlation.

## Settled decision

The first adapter is intentionally shadow-only. A changed project hook must be
reviewed/trusted by Codex before automatic use, and observed coverage is only
the local hook path documented by Codex.
