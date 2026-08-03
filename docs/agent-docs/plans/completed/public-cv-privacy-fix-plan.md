# Plan: Public CV Privacy Fix

**Status:** completed
**Created:** 2026-08-03
**Completed:** 2026-08-03

## Goal

Replace the public downloadable CV with a sanitised, current PDF that exposes no private-document access information, personal telephone number, email address, unpublished manuscript entry, or referee contact details.

## Design decisions

- Use the already approved two-page industry CV as the content baseline because the previous public PDF had no matching editable source.
- Preserve the existing job-application source and generate a separate public-CV source.
- Keep only the public website and ORCID as header contact routes.
- Do not alter or delete the encrypted document vault; remove every route and credential for it from the public CV and verify that the historical exposed code is obsolete.
- Preserve unrelated CMB work already present in the website worktree.

## Scope

- Add a separately maintained public-CV LaTeX source under the local job-application workspace.
- Replace `media/Long_CV.pdf` with the sanitised build.
- Verify extracted PDF text, link annotations, page count, visual layout, and the website repository diff.

## Phases

1. **Sanitise and rebuild — completed:** see `public-cv-privacy-fix-phase-1-complete.md`.

## Closing note

The published asset is sanitised and the historically exposed access code is not valid for the current encrypted vault. Broader content and link improvements are intentionally deferred.
