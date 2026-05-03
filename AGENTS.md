# Agent Configuration

## What This Repository Is

A personal academic website for Adrian Mag, hosted on GitHub Pages. It contains static HTML pages, CSS stylesheets, and media assets presenting research, publications, CV, and contact information.

## Plan Directory

All agent plan files are stored under:
- `plans/active-plans/` — current plans being worked on
- `plans/completed-plans/` — archived finished plans

## Living Reference Documents

Before modifying any page or stylesheet, read:
```
docs/agent-docs/references/living/website-reference.md
```

This file contains the page layout, CSS conventions, and file mappings for the entire site.

## Commit Convention

See `COMMIT_CONVENTION.md` for the full commit message format. All feature/fix commits must include plan references.

## Environment

This is a static website — no build step, no package manager, no tests. Validate changes by opening pages in a browser. There is no conda environment or Python code in this workspace.

## Key Conventions

- **No frameworks**: Plain HTML5 and CSS3 only. No JavaScript frameworks, no preprocessors.
- **Consistent styling**: Each page links its own CSS file (e.g., `about.css`) plus the shared `styles.css`.
- **Media paths**: Images and PDFs live under `media/`. Use relative paths from the page's location.
- **Navigation**: The site-wide navigation bar is replicated in each HTML page's `<nav>` section. Any nav change must be applied to all pages.
