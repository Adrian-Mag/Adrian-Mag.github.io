# Agent-Docs Map

This directory is the durable, provider-neutral record of agent-assisted work
in this repository. It is organised into protocols: each protocol owns one kind
of record and its own rules. Source, reproducible behaviour, Git state, and
current user instruction remain authoritative when a record disagrees with
them.

## Layout

```text
docs/agent-docs/
  PROTOCOL.md                 this cross-protocol map
  COMMIT_CONVENTION.md        repository commit-message convention
  plans/                      tracked plan lifecycle and plan history
  references/                 maintained architecture and source evidence
  citation-audit/             private local citation-evidence library protocol
  agent-ledger/               soft agent-work observation protocol
  control/                    ignored legacy local continuity overlay
```

Read a protocol only when its records are relevant:

- [`plans/PROTOCOL.md`](plans/PROTOCOL.md) owns plan creation, revision,
  completion, abandonment, and phase evidence.
- [`references/PROTOCOL.md`](references/PROTOCOL.md) owns living workspace
  descriptions, source evidence, and the compact reference index.
- [`citation-audit/PROTOCOL.md`](citation-audit/PROTOCOL.md) owns the private
  local-paper evidence route and its PDF-reading-skill boundary.
- [`agent-ledger/PROTOCOL.md`](agent-ledger/PROTOCOL.md) owns procedure
  evidence, safe event vocabulary, reporting semantics, and the ignored future
  local runtime boundary.
- `control/` is private, ignored live continuity machinery. It is not a tracked
  source of truth and will be retired or redistributed only through a separate
  migration.

## Cross-protocol rules

- Do not duplicate one record merely because another protocol needs it. A plan
  links to a source dossier or living reference; it does not copy it.
- Provider adapters (`AGENTS.md`, `.agents/`, `.claude/`, `.codex/`) are thin
  discovery bridges. Canonical agent documentation lives here.
- Feature, fix, and refactor commits follow `COMMIT_CONVENTION.md` and cite the
  governing plan path that was canonical at commit time.
- Historical Git commit messages are never rewritten when records later move.
- Keep private control state, prompts, transcripts, credentials, and local
  telemetry out of tracked agent documentation unless the user explicitly
  approves a privacy-reviewed record.
