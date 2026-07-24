# Agent-document reference

## Scope

This living reference describes the tracked and local-only structures that help
agents work in this website repository. It is a map of ownership and entry
points, not a transcript, a complete manual, or a replacement for source and
Git evidence.

## Authority and reading rule

Read this record when changing agent-document architecture, root agent
guidance, provider discovery bridges, or a protocol boundary. Read the relevant
subprotocol next; do not infer a subsystem's detailed rules from this overview.
Current user instruction, source, Git, and the referenced protocol outrank this
summary if they disagree.

## Current structure

```text
AGENTS.md                         automatic project entry instruction
docs/agent-docs/
  PROTOCOL.md                     cross-protocol map
  COMMIT_CONVENTION.md            commit traceability convention
  plans/                          plan lifecycle protocol and records
  references/                     this protocol, living records, dossiers
  citation-audit/                 private local citation-evidence protocol
  agent-ledger/                   soft procedure-observation protocol
  control/                        ignored legacy continuity bridge
.codex/, .claude/, .agents/       provider-specific discovery adapters
```

### Plans

`plans/` owns plan rules and plan history. `plans/active/` contains only live
plans; `plans/completed/` contains settled or abandoned plans and phase
evidence. Plans link to references rather than carrying source dossiers.

### References

`references/` owns current maintained descriptions and source dossiers.
`references/INDEX.md` selects the first relevant record. Living records are
updated with the structure they describe; source dossiers preserve provenance
and explicit verification gaps.

### Citation Audit Library

`citation-audit/` owns the route to this workspace's ignored local paper
library and previous citation-verification records. Its tracked protocol tells
an agent when that private evidence is relevant and requires the
`pdf-source-reading` skill before a local PDF is opened, extracted, or
rendered. The library is durable SSD material, not automatic context and not a
public source repository.

### Automatic entry and adapters

The root `AGENTS.md` is the durable, automatically discoverable project card.
It gives only stable workspace facts, critical boundaries, and pointers into
the canonical agent docs. `.codex/`, `.claude/`, and `.agents/` are thin
provider adapters: they may discover instructions, skills, or hooks, but they
must not become the sole owner of project facts or protocol rules.

### Agent Ledger

`agent-ledger/` owns soft observability rules: expected procedure evidence,
safe declared and host-observed event categories, reporting semantics, and an
ignored local `runtime/` boundary. Its tracked `scripts/ledgerctl.py` is the
only supported local writer and report generator; its tests use temporary
runtimes. Its thin Codex hook adapter is configured locally in shadow mode:
it safely correlates a prompt, exposed local tool events, and a later route
declaration when Codex trusts the changed project hook definitions. Coverage is
partial; it has no gate or strong anti-tamper boundary. The legacy control
telemetry remains operational until a separate migration.

### Legacy local bridge

`docs/agent-docs/control/` is ignored local continuity machinery. It remains
operational while plans and references are being separated, but it is not a
tracked authority and is not the target name for the future architecture.
Never stage, publish, or copy its contents into public documentation.

## Update triggers

Update this reference when protocol ownership changes, a canonical path moves,
an entry/adaptor boundary changes, or a new agent-document protocol becomes
real. Verify the named paths and read the relevant subprotocol before updating.
