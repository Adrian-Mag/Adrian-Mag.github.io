# Agent Configuration

## Local Control Bootstrap

When `docs/agent-docs/control/BOOTSTRAP.md` exists, read it once at the start or resumption of every task in this worktree and use the canonical `website-control` workflow it identifies. Validate the recorded repository, branch, commit, and dirty state before trusting `CURRENT.md` or `HANDOFF.json`. If that applicability check fails, stop workspace work, rebuild those notes from Git and source evidence, and revalidate before continuing. Refresh the handoff at meaningful task boundaries. The control overlay and its redacted validation-incident record are local-only and must never be staged, committed, served, or copied into public documentation.

## What This Repository Is

A personal academic website for Adrian Mag, hosted on GitHub Pages. It contains static HTML pages, CSS stylesheets, and media assets presenting research, publications, CV, and contact information. It also carries **offline research tooling** that is *not* served: LaTeX sources for the long-form notes (`*.tex` at the repo root) and a Python figure-generation pipeline under `figure_generation/` (see its `README.md`).

## Plans

Plan records and their lifecycle rules live under
`docs/agent-docs/plans/`. Read `docs/agent-docs/plans/PROTOCOL.md` before
creating, revising, completing, or archiving a substantial-work plan.

- `docs/agent-docs/plans/active/` — current plans being worked on
- `docs/agent-docs/plans/completed/` — archived plans and phase-completion records

## Reference Documents

Reference records and their update rules live under
`docs/agent-docs/references/`. Use `docs/agent-docs/references/INDEX.md` to
locate the smallest relevant record; read
`docs/agent-docs/references/PROTOCOL.md` before creating, renewing, or retiring
a reference.

Before modifying any page or stylesheet, read:
```
docs/agent-docs/references/living/website-reference.md
```

This file contains the page layout, CSS conventions, and file mappings for the entire site.

## Citation Audit Library

The private citation evidence library is described by
`docs/agent-docs/citation-audit/PROTOCOL.md`. Read it when verifying or
revising a citation or research claim using local source material. Before
opening, extracting, or rendering one of its local PDFs, use the
`pdf-source-reading` skill; it keeps source content on this machine and records
page-specific evidence. Never stage, serve, or upload the library contents.

## Agent Ledger

The soft Agent Ledger protocol lives under `docs/agent-docs/agent-ledger/`.
It records declared procedural evidence and independently observed events when
an adapter exists; it does not grant authority or replace plans and references.
Read its `PROTOCOL.md` when auditing or changing agent procedures, ledger
reporting, runtime, or a host-observation adapter. Use its canonical
`scripts/ledgerctl.py` for a ledger-relevant work phase; never manually edit
its ignored `runtime/` records. A trusted Codex project may add shadow
host observations through the local provider configuration; those are partial
evidence, not a complete activity trace.

## Commit Convention

See `docs/agent-docs/COMMIT_CONVENTION.md` for the full commit message format. All feature/fix commits must include plan references.

## Environment

The **served site** has no build step, no package manager, and no bundler — validate page/CSS changes by opening the HTML in a browser. The **figure-generation pipeline** (`figure_generation/`) is separate: it is Python, runs offline on demand through the `inferences` conda environment, writes assets into `media/`, and has its own pytest suite. It is never part of the deployed site.

One small offline step feeds the site: the client-side search (`pages/search.html`) reads a pre-built index at `media/search-index.json`. After editing any notes page, regenerate it with `python3 tools/build_search_index.py` (stdlib only, no conda env needed) and commit the refreshed JSON alongside the content change.

## Key Conventions

- **No frameworks**: Plain HTML5 and CSS3 only. No JavaScript frameworks, no preprocessors.
- **Consistent styling**: Each page links its own CSS file (e.g., `about.css`) plus the shared `styles.css`.
- **Media paths**: Images and PDFs live under `media/`. Use relative paths from the page's location.
- **Navigation**: The site-wide navigation bar is replicated in each HTML page's `<nav>` section. Any nav change must be applied to all pages.

Cache busting: local CSS/JS references carry a `?v=N` query. After changing any stylesheet or script, bump the version on its references (site-wide search-replace) so phones don't serve stale assets.
