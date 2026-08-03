# Public CV Evidence Expansion: Phase 1 Complete

**Completed:** 2026-08-03

## What changed

- Expanded both public-CV formats with one linked published paper and two manuscripts in preparation, listed by title and authors without private preview links.
- Added five curated technical-writing links covering discretisation, SOLA, measure-theoretic Bayesian inference, conjugate gradients, and research software and AI workflows.
- Added all six recent presentations with direct public artifact links; the HTML also links the EGU technical explainer and UKSEDI supplementary presentation.
- Linked the SensRay repository from the technical-leadership entry and made contextual links visibly identifiable in the HTML CV.
- Expanded the downloadable PDF from two to three pages and kept the technical-writing section together on its own final page.
- Updated the website living reference to describe the evidence-linked public CV and its privacy contract.

## Settled decisions

- The expanded PDF remains a concise three-page professional CV rather than attempting to reproduce every item on the website.
- Manuscripts in preparation are titles-only public evidence: no private routes, previews, credentials, or access instructions are exposed.
- An explicit PDF page break is retained because the automatic layout split the technical-writing section awkwardly between pages.
- Link styling is local to the CV page, so the shared stylesheet and cache-busting version do not need to change.
- The site search index was not rebuilt because its builder excludes the CV page; the existing dirty search-index file belongs to unrelated CMB work.

## Verification

- Built the LaTeX source with `pdflatex -interaction=nonstopmode -halt-on-error`; the final output is three pages with no build errors.
- Confirmed the rebuilt and served PDFs have the same SHA-256 hash.
- Extracted the served PDF text and confirmed there is no telephone number, email address, password/access-code wording, private-vault route, private-document label, or referee section.
- Enumerated PDF URI annotations, confirmed there are no private-vault URLs, and confirmed every website URL maps to a local public file.
- Parsed the HTML and confirmed all 31 local links resolve; external new-tab links retain `rel="noopener"`.
- Rendered and visually inspected the final PDF and desktop and mobile HTML layouts without clipping, overlap, or horizontal overflow.
- Ran focused whitespace and sensitive-string checks over the changed CV files.

## Verification skipped

- No live-site or other network check was run; local source files and the served PDF asset were used because this workspace is offline-only.

## Follow-up

- Align the older HTML Education, Experience, Research, and Technical Skills material with the current PDF, including the revised impact-led capability and scientific-software framing.
