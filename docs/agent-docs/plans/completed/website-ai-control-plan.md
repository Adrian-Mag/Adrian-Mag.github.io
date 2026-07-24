## Plan: website AI control pack
**Status:** completed   **Created:** 2026-07-21   **Completed:** 2026-07-21

### Goal

Adapt the proven `intervalinf` control-pack design to this website workspace so future AI
sessions can recover exact repository state, current work, evidence, risks, and the next safe
action without reconstructing a conversation. Preserve the repository's existing tracked
agent-docs protocol while keeping branch- and machine-specific control state private and out of
GitHub Pages.

### Design notes

- Source, Git state, deterministic checks, and human-approved tracked documentation outrank
  AI-maintained summaries.
- Canonical control state lives in ignored `docs/agent-docs/control/`; the existing tracked
  `plans/active/`, `plans/completed/`, and living references remain the durable project record.
- State is scoped to the exact repository root, branch, base commit, and dirty paths. A mismatch
  invalidates it until reviewed.
- One provider-neutral `website-control` skill owns startup, maintenance, and handoff. Claude,
  Codex, and generic-agent locations contain discovery adapters only.
- The validator uses Python's standard library and validates structure, JSON shape, Git
  applicability, ignore protection, evidence paths, and adapter targets. It cannot certify the
  semantic truth of the website or its prose.
- The first handoff must preserve the uncommitted Act 6 work already in the worktree and the
  unrelated untracked `convex-slide1.jpeg` without claiming ownership of either.

### Files / components

- `.gitignore`, `AGENTS.md`, and `docs/agent-docs/PROTOCOL.md`
- `docs/agent-docs/control/{CONTROL.json,PRINCIPLES.md,CURRENT.md,HANDOFF.json,MAINTENANCE.md,BOOTSTRAP.md}`
- `docs/agent-docs/control/skills/website-control/`
- `.agents/skills/website-control`, `.claude/skills/website-control`, and `.codex/config.toml`
- `.claude/rules/website-control.md`

### Phases

1. Record the adaptation boundary between tracked project documentation and ignored live control
   state.
2. Create principles, current-state, maintenance, manifest, and structured handoff records.
3. Create the canonical skill and thin provider discovery adapters.
4. Add deterministic validation and test both current and deliberately stale handoffs.
5. Update tracked bootstrap documentation, close the plan, and leave a validated handoff.

### Open questions

- Whether future use shows enough cross-provider friction to justify more adapters.
- Whether the current-state reference should eventually be generated in part from the tracked
  website living reference; the pilot begins with manual, evidence-linked curation.
- Which repeated omissions, if any, justify extending the handoff schema.

### Closing note

All five phases completed. The implementation preserves the tracked agent-docs hierarchy and
adds an ignored, exact-worktree control overlay with provider-neutral principles, current state,
structured handoff, maintenance rules, one canonical skill, Claude/Codex/generic discovery
adapters, and a standard-library validator. The validator passed for the live dirty worktree,
rejected a deliberately wrong commit, and reported that mismatch without failing only when
explicitly run with `--allow-stale`. No control file or adapter is tracked or staged. Future
extensions remain evidence-driven: add fields or automation only after real handoffs reveal a
repeated gap.
