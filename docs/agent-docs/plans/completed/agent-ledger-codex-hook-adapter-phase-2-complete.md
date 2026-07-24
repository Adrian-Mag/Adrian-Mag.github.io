# Agent Ledger Codex hook adapter — phase 2 complete

**Date:** 2026-07-24
**Plan:** `docs/agent-docs/plans/completed/agent-ledger-codex-hook-adapter-plan.md`

## Landed

- Added `agent-ledger/adapters/codex/codex_observer.py`, which reduces Codex
  hook payloads to safe event kinds and coarse tool classes.
- Added parallel local `.codex/config.toml` hooks for the new shadow observer
  while retaining the legacy control observer.
- Corrected the lifecycle meaning: `Stop` is a turn stop; `SessionEnd` is the
  true main-thread session end.

## Verification

- Adapter tests confirm prompt, transcript, cwd, arguments, and content fields
  do not reach the Ledger.
- Static configuration-shape check confirmed all eight configured hook events.
