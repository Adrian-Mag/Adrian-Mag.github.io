# Plan: Establish the references protocol

**Status:** completed
**Created:** 2026-07-24

## Goal

Make `docs/agent-docs/references/` the self-contained home for maintained
workspace descriptions and source-evidence records. The protocol will say how
references are found, updated, checked, and retired without turning them into
plans, session handoffs, or a duplicate of source code.

## Design decisions

- `living/` contains current, maintained descriptions of a named subsystem.
- `sources/` contains evidence dossiers: claim provenance, source dates,
  artifacts, and explicit verification gaps. A dossier is not a plan.
- `INDEX.md` is a compact need-to-record registry. It tells an agent the first
  relevant reference to open; it never instructs loading all references.
- A new `living/agent-docs-reference.md` describes the current architecture of
  the agent-document protocols and their thin provider bridges.
- Reference records link to source and Git for authority. They do not silently
  replace source, copy large source files, or become a session diary.
- A dedicated reference-management skill is deferred until the protocol has
  shown a real repetitive task that needs one.

## Scope

- `docs/agent-docs/references/`
- Root `docs/agent-docs/PROTOCOL.md` and `AGENTS.md`
- Existing local continuity instructions that name reference records
- Public harness pages that show the real agent-document tree
- Search index after explanatory prose changes

## Phases

1. **Create the protocol and registry.** Define reference kinds, authority,
   update triggers, verification, and retirement.
2. **Add current agent-document reference.** Record the present protocol map,
   entry points, and legacy-control boundary without publishing private state.
3. **Update entry points and public explanation.** Point root guidance and the
   explorer at the protocol; keep the Act 6 AGENTS popup verbatim.
4. **Verify and settle.** Check paths, static page structure, registry links,
   search index, and write completion evidence.

## Open questions

- Which repeated reference-review tasks justify a dedicated skill rather than
  the protocol and normal file tools?
- Whether later source dossiers need their own subfolders by project, or their
  filenames and the compact registry remain sufficient.

## Closing note

All four phases landed on 2026-07-24. References are now a self-contained
protocol with a compact dispatcher and an agent-document living reference. A
dedicated reference-management skill remains deliberately deferred until real
maintenance work demonstrates that the protocol alone is insufficient.
