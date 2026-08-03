# Plan: Public CV Evidence Expansion

**Status:** completed
**Created:** 2026-08-03
**Completed:** 2026-08-03

## Goal

Expand the general public CV into a stronger referral document for scientific and technical leads by adding the complete recent presentation record, two clearly labelled manuscripts in preparation, and curated links to public technical writing, while keeping the HTML and downloadable PDF aligned.

## Design decisions

- Expand the PDF from two to no more than three pages so the additional evidence does not crowd the principal experience and software sections.
- Link the published article to its DOI, presentation titles to public artifacts, and technical-writing titles to their public landing pages.
- List the two unpublished works by title and author list only as manuscripts in preparation; provide no preview links, passwords, access codes, or private-vault routes.
- Keep the existing public-CV privacy contract: no telephone number, email address, or referee contact details in the PDF.
- Add all six recent presentations to both versions, with the HTML retaining the more expansive descriptions and links.
- Preserve unrelated CMB work already present in the website worktree.

## Scope

- Update the separately maintained public-CV LaTeX source.
- Rebuild and replace `media/Long_CV.pdf`.
- Add publications and manuscripts, selected technical writing, and linked presentation evidence to `pages/cv.html`.
- Update the website living reference and run focused PDF, HTML, link, privacy, and visual checks.

## Phases

1. **Evidence expansion — completed:** see `public-cv-evidence-expansion-phase-1-complete.md`.

## Closing note

The HTML and PDF now expose the strongest current publication, manuscript, technical-writing, software, and presentation evidence while preserving the public-CV privacy contract. Broader rewriting of the older HTML experience and skills sections remains separate follow-up work.
