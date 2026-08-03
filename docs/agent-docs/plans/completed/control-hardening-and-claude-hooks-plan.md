# Plan: Control Hardening and Claude Hook Parity

**Status:** completed
**Created:** 2026-08-03
**Completed:** 2026-08-03

## Goal

Close four gaps found in the 2026-08-03 audit of the local website-control
overlay, so that the "validated" receipt means something closer to what a reader
assumes, and so both agents that touch this worktree are observed equally.

The audit found the overlay strong at privacy and version-scoped applicability
but silent on the two failures that actually occurred: a well-formed handoff
that omitted uncommitted work, and a content leak that reached a published
commit. It also found the telemetry blind to Claude Code, because only Codex has
lifecycle hooks.

## Scope

All machinery here lives in the git-ignored control overlay
(`docs/agent-docs/control/`, `.claude/`, `.codex/`); none of it is committed or
served. Only this plan and its completion record are tracked. `PRINCIPLES.md` is
not amended; observation-only mode is preserved (no new enforcement, model
calls, or background agents).

## Changes

1. **Honest receipt scope.** `controlctl.py` begin/close and the validator PASS
   line state what was actually checked — structure and Git applicability — and
   what was not: content safety, prose, and completeness of intent. Removes the
   false confidence that a green receipt implies a safe published site.

2. **Handoff completeness gate.** The validator gains a `handoff_completeness`
   check: when a handoff declares the work finished (`state.status` in
   `complete`/`ready_for_use`), every dirty or untracked path in the tracked
   worktree must be accounted for, either under `changes.*` or under
   `git.unrelated_paths`. This is the specific trap that let the prior session
   hand off a replaced CV PDF and four untracked plan files under a passing
   receipt. In-progress handoffs are exempt; `--allow-stale` bypasses for
   diagnostics.

3. **First-class sensitive-string sweep.** `controlctl.py sweep` scans the
   staged diff (optionally the worktree) for public IPv4 addresses, common
   credential and key formats, private-key blocks, and the known never-publish
   codename, returning non-zero on any hit. This promotes the manual habit that
   has been the only control actually catching leaks into a named step. It scans
   text diffs only; binary assets are explicitly out of range and the output
   says so.

4. **Claude hook parity + provider-neutral observer.** `codex_observer.py` is
   renamed `hook_observer.py` (it already maps both agents' tool names).
   `.claude/settings.json` wires the same lifecycle events Codex has, guarded so
   a hook can never block a tool call. The validator now requires and checks
   both adapters. The report and `MAINTENANCE.md` state honestly that
   `would_violate` counts patch-class mutation only, because detecting mutating
   shell commands would require inspecting command text the telemetry is
   forbidden to retain.

## Phases

1. **Implement and verify — completed:** see
   `control-hardening-and-claude-hooks-phase-1-complete.md`.

## Verification

- `test_control_telemetry.py` passes after the observer rename.
- Completeness gate: current handoff passes; a handoff with an unaccounted dirty
  path fails with `handoff_completeness` via `--handoff`.
- `controlctl.py sweep` returns non-zero on a seeded pattern and zero on a clean
  staged diff.
- `begin`/`close` succeed end-to-end with the renamed observer, updated
  `CONTROL.json`, and both adapters present.
- Private-path guard still passes: no control or adapter file is tracked or
  staged.

## Open questions

- Per-tool hooks add observer latency to every Claude tool call (three git
  calls plus file IO per event). Parity is delivered as requested; a
  lighter-weight identity computation is a possible follow-up if it proves slow.
- Enforcement (blocking on `would_violate`) remains deliberately out of scope
  and would need separate approval per the skill boundary.
