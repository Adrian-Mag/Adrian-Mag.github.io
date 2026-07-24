# Agent Ledger reporting

The local report groups events by opaque work phase and compares them with the
matching procedure. It reports facts and gaps, not hidden model reasoning.

```text
Declared route: inspect
Observed action class: patch
Finding: declared/observed mismatch; review required
```

```text
Procedure: default workspace work
Declared route: change-planned
Observed tool activity: present
Close event: absent
Finding: expected close evidence missing
```

Reports must say whether an event was agent-declared, host-observed, or
derived. They must not say that an agent "read", "understood", or "followed"
a procedure unless the available evidence genuinely supports that limited
claim. Reports are diagnostic in the first release; they do not block work.

## First reporter rules

`ledgerctl.py report` currently writes a derived `runtime/report.json` and
reports only two conservative gaps:

- host or Git activity without a declared route for that work phase;
- an open current phase without a declared close.

It deliberately does not report a route/action mismatch from an ordinary tool
event. Such a rule would need a human-approved definition of which action is
incompatible with which route.

## Codex shadow-adapter coverage

The adapter sees only the hook events Codex exposes through the trusted local
project configuration. In particular, a local `PreToolUse`/`PostToolUse` pair
can provide a coarse class for a shell command, patch, MCP call, or local
function, but hosted and specialized tool paths may not enter that hook path.
The report therefore describes local-hook evidence, not a complete trace of
everything the agent did.
