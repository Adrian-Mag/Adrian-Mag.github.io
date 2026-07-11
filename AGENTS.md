# Agent Configuration

## What This Repository Is

A personal academic website for Adrian Mag, hosted on GitHub Pages. It contains static HTML pages, CSS stylesheets, and media assets presenting research, publications, CV, and contact information. It also carries **offline research tooling** that is *not* served: LaTeX sources for the long-form notes (`*.tex` at the repo root) and a Python figure-generation pipeline under `figure_generation/` (see its `README.md`).

## Plan Directory

Agent planning follows the unified agent-docs protocol (`docs/agent-docs/PROTOCOL.md`). Plan files live under:
- `docs/agent-docs/active-plans/` — current plans being worked on
- `docs/agent-docs/completed-plans/` — archived finished plans

(The old top-level `plans/` directory has been retired.)

## Living Reference Documents

Before modifying any page or stylesheet, read:
```
docs/agent-docs/references/living/website-reference.md
```

This file contains the page layout, CSS conventions, and file mappings for the entire site.

## Commit Convention

See `COMMIT_CONVENTION.md` for the full commit message format. All feature/fix commits must include plan references.

## Environment

The **served site** has no build step, no package manager, and no bundler — validate page/CSS changes by opening the HTML in a browser. The **figure-generation pipeline** (`figure_generation/`) is separate: it is Python, runs offline on demand through the `inferences` conda environment, writes assets into `media/`, and has its own pytest suite. It is never part of the deployed site.

One small offline step feeds the site: the client-side search (`pages/search.html`) reads a pre-built index at `media/search-index.json`. After editing any notes page, regenerate it with `python3 tools/build_search_index.py` (stdlib only, no conda env needed) and commit the refreshed JSON alongside the content change.

## Key Conventions

- **No frameworks**: Plain HTML5 and CSS3 only. No JavaScript frameworks, no preprocessors.
- **Consistent styling**: Each page links its own CSS file (e.g., `about.css`) plus the shared `styles.css`.
- **Media paths**: Images and PDFs live under `media/`. Use relative paths from the page's location.
- **Navigation**: The site-wide navigation bar is replicated in each HTML page's `<nav>` section. Any nav change must be applied to all pages.

Cache busting: local CSS/JS references carry a `?v=N` query. After changing any stylesheet or script, bump the version on its references (site-wide search-replace) so phones don't serve stale assets.
