# Agent Ledger procedures

Procedures describe expected evidence for a kind of work. They do not dictate
the agent's private reasoning or grant authority that the user did not give.
They can be refined after real observations show a useful gap.

## Default workspace-work procedure

For a workspace-facing work phase, the expected evidence is:

```text
route declared
  → relevant durable record selected
  → work activity observed where the host exposes it
  → matching check declared or observed
  → affected plan/reference state updated when applicable
  → work phase closed
```

The appropriate record and check depend on the task:

- substantial work selects a plan through the plans protocol;
- current architecture or claim work selects a reference through the reference
  index;
- a conversation-only route may stop without a workspace work phase;
- a newly discovered need can reclassify the route before consequential work,
  but does not itself grant permission to edit.

## Interpreting incomplete evidence

Missing evidence means only that the ledger cannot show the expected step. It
may signal a skipped procedure, an unobserved action, an adapter gap, or an
inapplicable procedure. The report labels the gap; a human examines the task
and evidence before drawing a conclusion.

## Current command sequence

For a ledger-relevant workspace phase, use the canonical command rather than
editing runtime JSON by hand:

```bash
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py begin --route change-planned
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py record --record-type plan
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py step --step work
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py check --outcome passed
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py close
python3 docs/agent-docs/agent-ledger/scripts/ledgerctl.py report
```

The first command prints the opaque work-phase token. Later commands use the
open phase by default. `observe` is for a host or Git adapter, not a way for an
agent to describe its own work as independently observed.
