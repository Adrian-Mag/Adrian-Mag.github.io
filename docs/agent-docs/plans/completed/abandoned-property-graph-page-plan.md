# Plan: Physical-property / inference graph page (under construction)
**Status:** abandoned — taken offline 2026-09-22 at the author's request (IP containment ahead of
employment). Page, app bundle, stylesheet, overview card and llms.txt entry removed; the tool's
source and scientific database remain local-only in the Ascension workspace
(`tools/physical-property-graph/`, `npm run dev`). Safe follow-up if the page ever returns: this
plan's design decisions still hold; check git history before this date for the removed files.
**Created:** 2026-09-09

## Goal

Publish an early, clearly labelled prototype of the interactive physical-property /
geophysical-inference graph on the site so it can be shown to collaborators, including on a
phone, without implying it is finished.

## Design decisions

- The app is a **prebuilt static bundle** (Vite + React + Cytoscape, built elsewhere) dropped
  into `pages/research/overview/property-graph/app/`. Its source and scientific database live in
  the private Ascension research workspace (`tools/physical-property-graph/`), which builds the
  bundle with `npm run deploy:site`. The site keeps its no-build-step rule: nothing here is
  compiled; the bundle is served as plain files. The bundle's asset paths are relative, so it
  works under this subpath.
- It is served from `pages/…`, **not** `tools/`, because `_config.yml` excludes `tools/` from the
  live site.
- A **wrapper page** `pages/research/overview/property-graph/index.html` carries the site nav,
  hero, an explicit under-construction notice, a full-screen "open" button, and a desktop-only
  iframe preview. On narrow screens the iframe is hidden and the button is the route, because an
  embedded pan/zoom canvas inside a scrolling page is unusable on a phone.
- The app itself shows an "Under construction" banner (a build-time flag) with a link back to
  the wrapper page, so the status is visible even when the app URL is shared directly.
- Discoverability: a card on the research overview page and an `llms.txt` entry. **No global
  nav change** for a prototype (the nav is replicated in every page; that cost is deferred
  until the tool is stable).
- The wrapper page reuses the site theme (space/earth); the app reads the same
  `site-theme` localStorage key, so the two agree.

## Scope

In: wrapper page, page stylesheet, bundle directory, overview card, llms entry, search-index
list entry and rebuild, living-reference update. Out: nav changes, any edit to the app's
science (owned by the Ascension workspace), the withheld CMB page.

## Phases

1. Land the page, bundle, card, registry entries and reference update; verify desktop and
   narrow-width rendering; commit and push. — **complete**, see
   `../completed/property-graph-page-phase-1-complete.md`.
2. (Later) Refresh the bundle as the tool evolves: rerun `npm run deploy:site` in the
   Ascension workspace, bump the "Last updated" line on the wrapper page, commit `app/` as a
   whole. Promote to the global nav when the tool stabilises.

## Open questions

- When the tool stabilises: add it to the global nav dropdown (all pages) and decide whether the
  source repository becomes public.
- Whether to version the bundle (`app/`) in this repo long-term or move the tool to its own
  repository with its own Pages deployment and link out.
