# Plan: Establish the Agent Ledger protocol

**Status:** complete
**Created:** 2026-07-24

## Goal

Create `docs/agent-docs/agent-ledger/` as the self-contained home for soft
agent-work observability: procedures, event vocabulary, reporting rules, and
the local runtime boundary. Make the ledger visible from automatic entry and
the reference index without claiming that it already enforces behaviour.

## Design decisions

- The Agent Ledger records procedure evidence; it does not choose an agent's
  route, grant authority, replace plans/references, or expose private reasoning.
- Agent-declared events and independently host-observed events remain distinct.
  A report may compare them, but neither proves the agent read or understood a
  document.
- The tracked protocol, schema, procedures, and reporting rules live in
  `agent-ledger/`. Future local event state lives in its ignored `runtime/`
  subtree, not in plans or references.
- The existing ignored `control/` telemetry remains live legacy machinery.
  This phase creates no migration, gate, daemon, remote collector, or claim of
  tamper-proof local logging.
- `AGENTS.md` names the ledger as a soft observation protocol and directs an
  agent to its rules only when ledger/procedure work is relevant.

## Scope

- `docs/agent-docs/agent-ledger/`
- `.gitignore`, root agent-doc map, `AGENTS.md`, reference index, and
  living agent-document reference
- Public workspace explorer and Act 6 AGENTS popup
- Search index after explanatory-page prose changes

## Phases

1. **Define the ledger protocol.** Add the ownership, privacy, local-runtime,
   and non-enforcement boundaries.
2. **Define procedures and event schema.** Specify declared/observed events,
   a configurable default work procedure, and gap-report semantics.
3. **Wire canonical entry points.** Update AGENTS, the cross-protocol map,
   references index, living agent-doc map, and public explorer.
4. **Verify and settle.** Check paths, ignored runtime boundary, popup fidelity,
   static page structure, search index, and completion records.

## Open questions

- Which host events can a future provider adapter observe independently and
  reliably enough to map to this schema?
- What separate privilege or tamper-evidence boundary would be required before
  treating a local runtime ledger as stronger than cooperative self-reporting?
