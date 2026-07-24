# Plans Protocol

This protocol owns the workspace's **tracked plan records**: how substantial
work is proposed, followed, revised, settled, and made traceable in Git. It
does not own current architecture references, source dossiers, live local
handoff state, provider configuration, or action-observation records.

## Layout

```text
docs/agent-docs/plans/
  PROTOCOL.md       this contract
  active/           current working plans only
  completed/        completed/abandoned plans and phase records
```

## When a plan is required

Create a plan before substantial work: a new page or series, several related
components, a structural refactor, site-wide behaviour, substantial styling or
JavaScript, a publication/privacy boundary, expensive figure work, or an
agent-protocol redesign. Do not create a plan for a narrowly scoped correction,
status question, routine inspection, or one established validation command.

If small work becomes substantial, stop before the broader change and create
or revise the plan that will govern it.

## Creating an active plan

Create `active/<kebab-case-name>-plan.md`. A useful plan contains:

```markdown
# Plan: <title>
**Status:** active
**Created:** YYYY-MM-DD

## Goal
## Design decisions
## Scope
## Phases
## Open questions
```

The plan is a live working contract, not a session diary. Keep its goal,
current constraints, unfinished phases, and open questions current. Put
settled decisions and completed verification in a phase-completion record
instead of letting the active plan become an archive.

## Following and revising a plan

Before material work, identify the governing active plan and the current phase.
Read only the parts needed for that work. Revise the plan before continuing if
the user changes the goal or scope, evidence changes a material decision, a
new risk affects the design, or the work crosses into a new phase.

Plans may point to records owned by other protocols:

- `../references/` for living architecture and source evidence;
- the Agent Ledger, when present, for observed procedural evidence;
- Git and source for current workspace truth.

Those records are not copied into a plan merely for convenience.

## Completing a phase

When a phase lands, create:

```text
completed/<name>-phase-N-complete.md
```

It records what was done, meaningful deviations, decisions that became settled,
verification run, verification skipped, and follow-ups. Update the active plan
to show the next unfinished phase.

## Completing or abandoning a plan

When all work is complete, move the plan to `completed/`, change its status to
`completed`, and add a concise closing note. If work is consciously stopped,
move it to `completed/` as `abandoned-<name>-plan.md` with the reason and any
safe follow-up.

Never delete a plan or phase-completion record. The completed directory is the
durable decision and verification history.

## Commit traceability

Feature, fix, and refactor commits cite the plan that governed them, using the
path that was canonical at the time of the commit. See
`../COMMIT_CONVENTION.md` for the commit format. Do not rewrite historical Git
messages when a plan later moves from `active/` to `completed/`.

## Hygiene

Periodically review active plans untouched for more than 30 days. Complete,
abandon, or explicitly reactivate each one. Investigate a plan/reference
disagreement using current source and Git before changing either record.
