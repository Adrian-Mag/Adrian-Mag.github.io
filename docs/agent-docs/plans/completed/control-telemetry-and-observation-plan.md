## Plan: Local control telemetry and Codex observation harness
**Status:** completed   **Created:** 2026-07-23   **Completed:** 2026-07-23

### Goal

Make the local `website-control` workflow observable without claiming access to
the model's private reasoning. Record privacy-safe lifecycle and tool evidence,
let agents inspect a compact report when they are changing agent infrastructure,
and retain an audit baseline before any blocking gate is considered.

### Design notes

- Codex is the only integrated client in this phase. The data format and
  `controlctl` commands remain ordinary JSON and standard-library Python so a
  later Claude adapter can use them.
- Events are local-only and redacted: no prompts, transcripts, shell commands,
  raw paths, file contents, tool output, credentials, or network data. A
  pseudonymous session correlation value is sufficient for coverage counts.
- The first release is observation-only. Hooks can report would-be violations
  but may not deny an action. Promotion to mutation or commit gates requires a
  later explicit review of a real baseline report.
- The detailed rolling ledger retains 500 events; aggregate monthly totals
  survive trimming. Public website maps remain unchanged until evidence exists.

### Files / components

- `docs/agent-docs/control/` — ignored manifest, telemetry state, control CLI,
  validator integration, Codex hook adapter, and local tests.
- `.codex/config.toml` — ignored Codex lifecycle hook registration.
- `docs/agent-docs/plans/active/` and `plans/completed/` — tracked plan and
  phase-completion evidence only.

### Phases

1. **Control contract and telemetry core.** Completed; see
   `control-telemetry-and-observation-phase-1-complete.md`.
2. **Codex observation adapter.** Completed; see
   `control-telemetry-and-observation-phase-2-complete.md`.
3. **Evidence and handoff.** Completed; see
   `control-telemetry-and-observation-phase-3-complete.md`.

### Closing note

The observation baseline is ready. Enforcement thresholds, Claude integration,
remote attestation, and any public-map revision remain deliberately separate
human-approved work after real telemetry is reviewed.
