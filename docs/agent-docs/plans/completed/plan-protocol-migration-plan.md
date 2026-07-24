# Plan: Establish the plans protocol

**Status:** completed
**Created:** 2026-07-24

## Goal

Make `docs/agent-docs/plans/` the self-contained home for every tracked plan
record in this workspace. The protocol must explain how plans are created,
followed, revised, completed, abandoned, and linked to commits, while leaving
other agent-document systems to own their own records.

## Design decisions

- `plans/active/` contains only live plans. `plans/completed/` contains
  completed or abandoned plans and phase-completion records.
- `plans/PROTOCOL.md` owns plan lifecycle rules. Root `agent-docs` guidance
  stays a short map of the protocols; it does not duplicate plan rules.
- Plans remain Markdown for this workspace. This is a workspace choice, not a
  claim that every harness must use this format.
- A source dossier is evidence, not a plan. The Machine Around the Model
  dossier moves to `references/sources/` and remains linked from its plan.
- Current references and public explanatory pages must use the new canonical
  paths. Historical Git commit messages remain unchanged.
- No provider-adapter or ignored `control/` migration happens in this plan.

## Scope

- `docs/agent-docs/plans/`
- Existing tracked and untracked plan records under the old plan directories
- Root protocol, AGENTS instruction, commit convention, and live references to
  plan paths
- Harness pages that deliberately show the workspace agent-document structure
- Search index after their prose changes

## Phases

1. **Create the plan protocol and destination layout.** Define plan roles,
   lifecycle, completion evidence, naming, and the relationship to commits and
   other protocols.
2. **Migrate plan and dossier records.** Move active/completed records to the
   new hierarchy; move the dossier to references; update all live document
   links without rewriting historical Git messages.
3. **Update entry points and public explanation.** Update root agent guidance,
   commit documentation, relevant harness pages/maps, and the search index.
4. **Verify and settle.** Check for stale live paths, review the resulting
   hierarchy, run focused page checks, and write the phase-completion record.

## Open questions

- Whether plan-management becomes a separately discoverable skill once the
  references and Agent Ledger protocols have their own canonical locations.
- Whether a later plan index is needed, or filenames plus `active/` remain a
  sufficient dispatcher for this workspace.

## Closing note

All four phases landed on 2026-07-24. The plan protocol is now a dedicated
subsystem; the references protocol and Agent Ledger remain separate future
work. The legacy ignored `control/` overlay was kept operational and had its
live plan-path pointers updated, but was not otherwise redesigned here.
