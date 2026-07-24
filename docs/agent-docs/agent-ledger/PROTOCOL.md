# Agent Ledger Protocol

The Agent Ledger is a **soft agent-work observability protocol**. It records
the steps an agent declares it took and, where a host can provide them, events
independently observed outside the agent's decision loop. Its purpose is to
make a workspace procedure inspectable later.

It is not a route chooser, an authority system, a plan, a reference library, a
skill, a subagent, or a hook. Skills and hooks may later implement parts of the
protocol; neither is the protocol itself.

## Layout

```text
docs/agent-docs/agent-ledger/
  PROTOCOL.md       this contract
  PROCEDURES.md     expected sequences of evidence
  EVENT_SCHEMA.md   declared and observed event vocabulary
  REPORTING.md      how gaps and reports are interpreted
  scripts/          canonical runtime writer and reporter
  adapters/codex/   thin Codex hook payload reducer
  tests/            focused runtime checks
  runtime/          ignored local events, state, and reports
```

## What the ledger records

- **Agent-declared events:** an agent's stated route, record selection,
  procedure steps, reclassification, checks, and close.
- **Host-observed events:** exposed host, tool, Git, or other deterministic
  lifecycle events.
- **Derived findings:** a deterministic report may identify missing expected
  evidence or a declared/observed mismatch.

An agent declaration is useful evidence, not proof. A host observation is
independent of the declaration, not proof that the agent understood a file or
made a correct decision. Absence of an event is not proof of misconduct.

## Procedure ownership

`PROCEDURES.md` defines the expected evidence for a named kind of work. A
procedure may mention plans and references, but those protocols retain
ownership of their records. The ledger records that a relevant step was
declared or observed; it does not copy the plan or reference into its own
state.

## Runtime and privacy boundary

`runtime/` is ignored local state for `events.jsonl`, `state.json`, and
`report.json`. It must never be staged, served, or copied into public
documentation. Tracked documents define schemas, rules, and the code that
writes the local state.

No ledger event may contain prompt text, hidden reasoning, command text, raw
paths, file contents, tool output, credentials, session transcripts, or other
private material. `EVENT_SCHEMA.md` defines the permitted metadata.

## Current capability

`scripts/ledgerctl.py` is the canonical local writer and reporter. It accepts
only controlled categories and opaque work-phase tokens, writes compact state,
and rejects transcript-like fields. It serializes local event/state changes
with an advisory lock so concurrent hook commands do not normally lose records.

The Codex adapter under `adapters/codex/` is configured in the ignored local
`.codex/config.toml` as a shadow observer beside the legacy control telemetry.
It creates a pending opaque phase when Codex reports a submitted prompt; a later
`ledgerctl begin` claims that same phase for the agent's route declaration.
It records only the supported local-hook events. The adapter needs Codex's
project-hook trust before it runs, cannot observe every Codex tool path, does
not block work, and is not a tamper-proof audit trail.

## Future implementation boundary

The same unrestricted OS principal can still alter a local ledger. Any stronger
claim requires a separate privilege, signer, or append-only service and a
dedicated approved plan.
