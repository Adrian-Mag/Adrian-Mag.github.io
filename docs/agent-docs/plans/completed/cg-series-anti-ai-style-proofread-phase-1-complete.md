# CG series anti-AI-style proofread — completion record

**Plan:** `docs/agent-docs/plans/completed/cg-series-anti-ai-style-proofread-plan.md`
**Completed:** 2026-07-29

## Delivered

- Reviewed the overview and Acts 1–6 of *The Road to Conjugate Gradients*.
- Removed all 158 HTML `&mdash;` entities and all 29 Unicode em dashes from
  the series, including titles, metadata, callout labels, and reader-facing prose.
- Made two additional local style edits: removed “very” from “the very first
  experiment” and removed the generic transition “Hence”.
- Regenerated `media/search-index.json`.

## Verification

- No `&mdash;`, Unicode em dash, or triple-hyphen form remains in the seven
  CG HTML files.
- Python's standard HTML parser read all seven files without error.
- `git diff --check` passed for the changed CG files and search index.

## Not run

- No browser pass was needed: this is text and metadata only, with no layout,
  CSS, or JavaScript change.

## Follow-up

The temporary snapshots under `/tmp/cg-series-preproofread/` can be compared
with the working files before the normal commit flow.
