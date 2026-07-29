# Plan: CG series anti-AI-style proofread

**Status:** completed
**Created:** 2026-07-29
**Completed:** 2026-07-29

## Goal

Apply a minimal, meaning-preserving anti-AI-style proofread to *The Road to
Conjugate Gradients*: the overview and Acts 1–6. Remove every em dash from
reader-facing prose and make only narrowly local stylistic improvements.

## Design decisions

- Treated `&mdash;`, Unicode em dashes, and `---` used as prose punctuation
  as em-dash forms to remove. En dashes used for numeric ranges were preserved.
- Used commas, colons, or sentence breaks according to the local grammar. No
  mathematical content, citations, page structure, figures, or navigation changed.
- Rebuilt the search index because the affected files are notes pages.

## Scope

- `pages/research/overview/cg/conjugate-gradient.html`
- `pages/research/overview/cg/act-1.html` through `act-6.html`
- `media/search-index.json` (regenerated)

## Completion

All three phases completed. The baseline snapshots remain local at
`/tmp/cg-series-preproofread/` for review or rollback during this session.
