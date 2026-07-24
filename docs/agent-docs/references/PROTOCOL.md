# References Protocol

This protocol owns the workspace's **tracked reference records**: maintained
descriptions of the current workspace and dossiers that preserve evidence for
claims, dates, artifacts, and provenance. It does not own plans, session
handoffs, private telemetry, provider configuration, or the source code that a
reference describes.

## Layout

```text
docs/agent-docs/references/
  PROTOCOL.md       this contract
  INDEX.md          compact need-to-record registry
  living/           current maintained subsystem descriptions
  sources/          claim, artifact, and provenance dossiers
```

## Reference kinds

### Living references

`living/<topic>-reference.md` describes a current subsystem. It should state:

- scope and authority boundaries;
- when an agent should read it;
- the relevant file/component map and invariants;
- current conventions and update triggers;
- focused checks that establish the description remains trustworthy.

Update an affected living reference in the same unit of work as the structural
change it describes. Do not bulk-generate living references after the fact;
that makes them look complete while silently drifting from source.

### Source dossiers

`sources/<topic>-sources.md` preserves evidence rather than operational state.
It records verified source details, dates, artifact provenance, explicit
caveats, and gaps that must not be filled from memory. A source dossier may be
read before drafting a public claim, but it does not tell an agent how to plan
or execute the work.

## Finding a reference

Start with `INDEX.md`, then read the smallest record that answers the task. The
index is a dispatcher, not startup context and not an instruction to load all
reference material.

## Authority and checking

Current user instruction, source files, reproducible behaviour, Git state, and
the verified primary source outrank a reference record. If they disagree, mark
the reference stale or correct it from evidence; do not rationalise the
disagreement away.

Before relying on a reference, check its stated scope and the task's relevant
source. Before changing a reference, identify the evidence that changed. A
useful update says what was checked, what remains unknown, and what future
change would require another review.

## Creating, retiring, and linking records

Create a living reference only when a subsystem is repeatedly costly or risky
to rediscover. Link to records owned by other protocols instead of copying them:

- plans live in `../plans/`;
- source and Git remain evidence for current implementation truth;
- private live continuity and observation state stays outside tracked
  references unless explicitly privacy-reviewed.

Retire a reference by moving it to a future archive location with a replacement
pointer and reason. Never leave a stale document looking current.

## Privacy

Do not place prompts, transcripts, credentials, raw private logs, or ignored
live telemetry in tracked references. A dossier may identify a local artifact
only when the record is safe to track and does not publish the artifact itself.
