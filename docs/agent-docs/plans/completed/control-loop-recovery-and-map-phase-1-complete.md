## Control loop recovery and anatomy map — Phase 1 complete

**Plan:** `docs/agent-docs/plans/completed/control-loop-recovery-and-map-plan.md`
**Completed:** 2026-07-22

### Done

- Added private, ignored validation-incident ledger and summary entrypoints.
- Made validator failures carry safe categories; the records retain no raw Git
  values, paths, prompts, or file contents.
- Added the strict stop, repair-from-evidence, and revalidate route to the
  canonical skill, maintenance guide, and root workspace instruction.
- Added the explicit small/follow/revise/new-plan decision and phase-landing
  close route.

### Settled decisions

- A failed applicability check blocks ordinary workspace work until a rebuilt
  control packet passes again.
- Detailed incident history is capped at the newest 100 local events; durable
  opened/resolved, month, and category totals remain available locally.

### Verification

- The control validator passed with `--no-incident-update`.
- The incident report showed zero opened, resolved, and active events in the
  initial local ledger.
- Python compilation of the validator passed.

### Deviations

None.
