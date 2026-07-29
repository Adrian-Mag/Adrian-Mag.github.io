# Remaining research notes anti-AI-style proofread — completion record

**Plan:** `docs/agent-docs/plans/completed/remaining-research-notes-anti-ai-style-proofread-plan.md`
**Completed:** 2026-07-29

## Delivered

- Reviewed 54 HTML pages across the Bayes, Frequentist, Think First, SOLA, and
  harness research-note series.
- Removed 704 prose em-dash forms identified at inventory, including page titles,
  metadata, callout labels, and reader-facing prose.
- Removed the one literal “Most importantly,” style opener found in scope.
- Regenerated `media/search-index.json`.

## Verification

- No `&mdash;` or Unicode em dash remains in the 54 scoped HTML pages.
- No configured literal hedge, throat-clearing, recap-and-pivot, or
  utilise/leverage pattern remains in scope.
- Python's standard HTML parser read all 54 pages without error.
- `git diff --check` passed for the edited pages.

## Preserved intentionally

- The YAML `---` delimiters in the displayed code block of
  `harness/act-7.html` remain unchanged. They are code syntax, not prose
  punctuation.

## Not run

- No browser pass was needed because no layout, CSS, or JavaScript changed.

## Follow-up

The temporary snapshots under `/tmp/research-notes-preproofread/` are
available for a per-file diff review before committing.
