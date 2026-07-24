# Website AI Control Pack Complete

**Completed:** 2026-07-21
**Base product branch:** `main`
**Base product commit:** `3652d7ed299e49db397472d8d254f610f377f3e9`
**Worktree state:** provisional and dirty with the pre-existing Act 6 work

## Delivered

- Human-controlled, provider-neutral principles.
- A concise current-workspace reference scoped to the exact worktree, branch, base commit, and
  dirty state.
- A structured handoff that separates product files, tracked agent documentation, and ignored
  control files, and preserves unrelated untracked work explicitly.
- Maintenance, invalidation, task-scale, current-state refresh, and handoff-acceptance rules.
- One canonical `website-control` skill initialized with the skill-creator tooling and then
  stripped of provider-specific UI metadata.
- Ignored Claude, Codex, and generic-agent discovery adapters.
- A standard-library validator for manifest entry points, handoff schema and tracked-plan links,
  Git applicability, current-state metadata, evidence paths, ignore protection, staged/tracked
  leakage, adapters, and bootstrap instructions.
- Tracked bootstrap integration in `AGENTS.md`, `.gitignore`, and the agent-docs protocol.

## Evidence

- Skill quick validation: passed.
- Validator compilation: passed.
- Direct control validation: passed for dirty `main` at base commit `3652d7e`.
- Deliberately stale handoff: rejected because its commit did not match.
- The same stale handoff with explicit `--allow-stale`: reported `STALE` and passed structural
  validation, proving the inspection escape hatch is distinct from normal trust.
- Private path ignore checks: passed.
- Private tracked/staged checks: passed.
- Provider adapter target checks: passed.
- Generated validator bytecode cache: removed.

The full site audit was not rerun because the control pack does not alter served behavior. The
focused Act 6 browser, HTML, links, search-index, cache, and privacy checks recorded in the live
handoff remain the applicable product evidence.

## Adaptation from intervalinf

The intervalinf pilot ignores its entire agent-document tree. This website intentionally tracks
plans and living references, so the adaptation ignores only `docs/agent-docs/control/` and the
provider adapters. Its validator therefore forbids tracking of the private overlay without
rejecting the repository's existing public plans and references. Package-version and test-suite
checks were replaced by static-site evidence paths, cache/search workflows, and explicit
protection of unrelated dirty state.

## Next observation

Use the pack during the next real resume or provider handoff. Record omissions and maintenance
cost in the handoff itself; extend the schema only for repeated, observed friction.
