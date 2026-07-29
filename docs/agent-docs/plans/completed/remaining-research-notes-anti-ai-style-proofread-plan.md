# Plan: Remaining research notes anti-AI-style proofread

**Status:** completed
**Created:** 2026-07-29
**Completed:** 2026-07-29

## Goal

Apply the same meaning-preserving anti-AI-style proofread used for *The Road
to Conjugate Gradients* to every other multi-page research-note series:
Bayes, Frequentist, Think First, SOLA, and The Machine Around the Model.

## Design decisions

- Removed prose em-dash forms (`&mdash;` and Unicode em dash) while preserving
  en dashes used for numeric ranges and `---` YAML delimiters in a displayed
  code example.
- Made only local punctuation or clearly formulaic-style corrections. No claims,
  mathematics, citations, figures, navigation, CSS, or JavaScript changed.
- Rebuilt the search index after the note edits.

## Scope

- `pages/research/overview/bayes/` (11 pages)
- `pages/research/overview/frequentist/` (6 pages)
- `pages/research/overview/think-first/` (10 pages)
- `pages/research/overview/sola/` (12 pages)
- `pages/research/overview/harness/` (15 pages)

## Completion

All phases completed. Local baseline snapshots remain at
`/tmp/research-notes-preproofread/` for this session.
