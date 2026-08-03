# Public CV Privacy Fix: Phase 1 Complete

**Completed:** 2026-08-03

## What changed

- Replaced the old three-page public CV with a two-page PDF generated from the already approved current industry-CV content.
- Removed the telephone number, email address, unpublished-manuscript entries, private-vault links, access-code text, and referee names and contact details.
- Retained only the public website, ORCID, and selected public scientific-software links.
- Added a separately maintained LaTeX source for the public build outside the served website repository.
- Recorded the sanitised public-PDF contract in the website living reference.

## Settled decisions

- The encrypted document vault itself remains unchanged because the access code exposed by the historical public CV does not decrypt the current vault canary; the vault had already been re-keyed.
- Broader CV content, HTML restructuring, and additional portfolio links remain follow-up work rather than part of this privacy fix.

## Verification

- Built the standalone LaTeX source twice with `pdflatex -interaction=nonstopmode -halt-on-error`; output was two pages with no build errors.
- Extracted final served-PDF text and confirmed no email marker, UK telephone prefix, password/access-code wording, private-vault route, manuscript-in-preparation wording, or referee names remained.
- Enumerated every PDF URI annotation and confirmed the allowlist contains only the public website, ORCID, and public GitHub destinations.
- Confirmed the built and served PDFs have identical SHA-256 hashes.
- Rendered and visually inspected both final PDF pages; layout is readable with no clipping or overlap.
- Recovered the historical exposed code without printing it and verified locally that it does not decrypt the current vault canary.

## Verification skipped

- No live-site or network check was run; the local website source and served asset were the authority for this phase.

## Follow-up

- Expand and align the HTML and PDF CV content, then add curated links to publications, software, technical notes, AI notes, and presentations.
