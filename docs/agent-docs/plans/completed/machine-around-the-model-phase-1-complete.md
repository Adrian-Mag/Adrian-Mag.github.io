# Phase 1 complete — "The Machine Around the Model"

**Plan:** `docs/agent-docs/plans/active/machine-around-the-model-plan.md`
**Phase:** 1 — Skeleton
**Completed:** 2026-07-18

## What was done

- Created `pages/research/overview/harness/` with 13 pages: the landing page
  (`the-machine-around-the-model.html`), `act-1` … `act-11`, and `summary`. Each act page
  carries its movement, its planned interactive panel, and its planned artifact, so the
  skeleton is informative to navigate before any prose exists.
- Added `css/harness.css`, reusing the act-band / act-chip system from
  `think-first-discretize-later.css`, plus series-specific classes: `.hz-panel`
  (interactive shells), `.hz-exhibit` (artifact display), `.hz-versioned` (the date-marked
  call-outs required by plan decision D3), `.hz-illustrative` (the label the Act 2 tokenizer
  panel must carry per R4), and `.hz-draft` (temporary skeleton marker, to be removed as acts
  are written).
- Inserted a new **AI in Practice** nav group into all 56 pre-existing pages carrying the
  nav dropdown, grouping the AI-Assisted Research poster with the new series and leaving the
  five inverse-theory series under **Notes**. Each file's relative-path prefix was derived
  from its own existing SOLA link rather than assumed — five distinct prefixes exist in the
  tree.
- Added a **Notes on AI in Practice** section to `index.html`, separate from
  "Notes on Inverse Theory & Inference" (plan Q1).
- Registered the series in `tools/build_search_index.py` and rebuilt `media/search-index.json`.
- Reverted the in-progress `DPhil Student` edit in `index.html` back to `PhD Candidate`, per
  the author's decision, restoring site-wide consistency (verified: no `DPhil` remains).
- Added `.playwright-mcp/` to `.gitignore`.

## Deviations from the plan

1. **`tools/build_search_index.py` required a code change.** The plan listed "rebuild the
   search index" as a Phase 6 step but did not anticipate that `SERIES_DIRS` is an explicit
   allowlist — a new series directory is invisible to search until registered. Caught because
   the first rebuild reported 0 harness records despite the pages existing. Registered in this
   phase rather than deferring, since a silent gap would be easy to miss later.
   **Living-reference implication:** any future series needs this registration step; worth
   recording in `references/living/website-reference.md` when that file is next touched.

2. **No cache-bust version bump.** `AGENTS.md` requires bumping `?v=N` after changing a
   stylesheet or script. No existing CSS or JS file was modified — `harness.css` is new, and
   the nav edit is HTML — so no bump was warranted. Recorded here to show the rule was
   considered rather than overlooked.

3. **Landing-page lede rewritten** after author revision. The author supplied a stronger
   framing (responsibility shifted to the reader: *are we asking the right question, are we
   supplying the context?*), which was adopted. Three capability claims in the supplied draft
   were **not** carried over — "used to prove new mathematical results", "masters
   undergraduate level mathematics", and "getting ever closer to mastering PhD level
   mathematics" — on two grounds: they are unsourced (violating the plan's standing rule that
   no claim ships uncited) and the third is capability forecasting, explicitly excluded by
   Q7. Noted as a candidate for the Summary if properly sourced later.

## Evidence

- HTTP check: landing, `act-4`, `act-8`, `summary`, and `css/harness.css` all return 200.
- **Link integrity: 69/69** series links resolve to a real file, verified by resolving each
  `href` relative to its own containing file across all five path depths. 0 broken.
- Browser render verified on the landing page and `act-8`: hero, sticky act-chip nav with
  correct active state, prev/next, draft blocks with planned panel and artifact.
- **0 console errors.**
- Nav order verified in the DOM: Publications, Presentations, — AI in Practice — ,
  AI-Assisted Research, The Machine Around the Model, — Notes — , then the five series.
- Search index: **46 → 59** records; all 13 harness pages present and attributed to the
  series "The Machine Around the Model".

## Follow-ups

- `references/living/website-reference.md` needs the new series added (page map + the
  `SERIES_DIRS` registration requirement) — deferred to the phase that writes real content,
  so the reference describes something real rather than placeholders.
- Search results for this series will be thin until the acts are written; expected.
- Q8 (11 acts is one or two more than any shipped series; merge candidates Act 4+5 or
  10+11) remains open, deferred until drafting shows whether the length is real.

## Next

Phase 2 — Movement I (Acts 1–3). Recommended ordering within the phase: build the Act 3
statelessness demo **before** writing prose. It is the series' load-bearing reveal and its
highest-risk interactive element; if the interaction does not land, the structure of
Movement I changes, and the surrounding prose is better written to a working demo than the
reverse.
