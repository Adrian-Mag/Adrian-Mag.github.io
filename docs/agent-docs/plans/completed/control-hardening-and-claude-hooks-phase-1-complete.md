# Control Hardening and Claude Hook Parity: Phase 1 Complete

**Completed:** 2026-08-03

## What changed

All machinery is in the git-ignored control overlay; only this record and the
plan are tracked.

- **Honest receipt scope.** `controlctl.py begin` and `close`, and the
  validator's PASS line, now state what is checked (structure, Git
  applicability, handoff completeness) and what is not (content safety, prose,
  citations). `close` also reminds the operator to run the sweep.
- **Handoff completeness gate.** `validate_control.py` now fails a handoff whose
  `state.status` is `complete` or `ready_for_use` if any dirty or untracked path
  in the tracked worktree is absent from both `changes.*` and
  `git.unrelated_paths` (category `handoff_completeness`). In-progress handoffs
  are exempt; `--allow-stale` bypasses.
- **First-class sweep.** `controlctl.py sweep [--worktree]` scans added diff
  lines for public IPv4 addresses, common credential/key formats, private-key
  blocks, and the known never-publish codename, exiting non-zero on any hit.
  Text diffs only; binary assets are explicitly excluded in the output.
- **Claude hook parity.** `codex_observer.py` was renamed `hook_observer.py`
  (provider-neutral; it already mapped both agents' tool names).
  `.claude/settings.json` wires SessionStart, UserPromptSubmit, PreToolUse,
  PostToolUse, PreCompact, and Stop to it, each guarded with `|| true` so a hook
  can never block a tool call. `CONTROL.json`, the validator's file and
  entrypoint lists, and `.codex/config.toml` were updated to the new name; the
  separate Agent Ledger observer was left untouched. The validator now requires
  and checks both adapters.
- **Honest reporting.** The report and `MAINTENANCE.md` state that
  `would_violate` counts patch-class mutation only and is a floor, because
  classifying shell mutation would require inspecting forbidden command text.

## Settled decisions

- Observation-only mode is preserved for both agents. Enforcement (blocking on a
  would-be violation) was deliberately not added; it would need separate
  approval under the skill boundary.
- The completeness gate keys on `state.status` so it never blocks legitimate
  in-progress resumes, only handoffs that claim to be finished.
- The sweep detects sensitive IPv4 by classifying octets (excluding loopback,
  private, link-local, broadcast) rather than embedding the specific
  never-publish address in a file.
- `PRINCIPLES.md` was not amended.

## Verification

- `test_control_telemetry.py`: 5 tests pass, including a new Claude `Edit`
  payload mapping to patch-class and the sensitive-IP classifier.
- Completeness gate, negative: the full validator failed with
  `handoff_completeness` on the real untracked plan file before it was committed.
- Completeness gate, positive: with the plan file accounted, the full validator
  passed end-to-end.
- Sweep, positive: a staged scratch file with a fake Anthropic key, a public
  test IP, and the codename produced three flagged lines and exit 1, while
  private and loopback addresses on the same line were correctly ignored.
- Sweep, negative: a clean staged diff returned exit 0.
- The renamed observer processed a Claude `Stop` payload from stdin, wrote a
  redacted `session.stopped` event (hashed session, no path), and exited 0.
- `begin`/`close` ran end-to-end against the renamed pack with both adapters
  present; private-path guard confirmed no control or adapter file is tracked or
  staged.

## Verification skipped

- No live multi-tool Claude session was run to measure real per-tool hook
  latency; the cost is noted as an open follow-up rather than measured here.

## Follow-up

- If the per-tool Claude hooks prove slow (three git calls plus file IO per
  event), replace `identity()` with a lighter-weight computation that reads
  `.git/HEAD` directly, keeping the correlation hash stable.
- Enforcement mode remains a separate, approval-gated future step.
