# Property-graph page — Phase 1 complete
**Plan:** `docs/agent-docs/plans/active/property-graph-page-plan.md`
**Completed:** 2026-09-09

## What landed

- `pages/research/overview/property-graph/index.html`: wrapper page with the standard nav
  (copied from the CMB page, no nav additions), research hero, an "Under construction" notice
  (`.pg-construction`, warm accent), a full-screen button to `app/`, a desktop-only iframe
  preview, and a two-card reading guide. Hidden below 760px: the iframe (`.pg-frame-wrap`),
  because a pan/zoom canvas inside a scrolling page is unusable on a phone; the button remains.
- `css/property-graph.css` (`?v=1`): page-only stylesheet, tokens from `theme.css`.
- `pages/research/overview/property-graph/app/`: prebuilt Vite bundle (index.html, favicon,
  `assets/` with hashed JS/CSS and KaTeX fonts; 2.3 MB). Built in the Ascension workspace with
  `npm run deploy:site`, which sets `VITE_BANNER` (the in-app "Under construction" banner) and
  `VITE_SITE_HOME=../index.html` (the banner's back link), then rsyncs `dist/` here.
- `pages/research/overview/index.html`: new "Interactive tools / Work in progress" section
  with one card, placed above "Codes".
- `llms.txt`: entry under Research.
- `tools/build_search_index.py`: wrapper page added to `EXTRA_PAGES`; `media/search-index.json`
  rebuilt (62 → 63 pages). The CMB directory stays excluded, so no in-progress CMB text entered
  the index.
- `docs/agent-docs/references/living/website-reference.md`: directory layout, CSS pairing,
  page inventory.

## Decisions settled

- Served from `pages/`, not `tools/` (`_config.yml` excludes `tools/`).
- No global nav entry for a prototype; discoverability is the overview card + llms.txt.
- The app's source and scientific database stay in the private Ascension workspace; this repo
  only holds the built bundle. Rebuild there, never hand-edit `app/`.
- The bundle keeps its own styles and reads the site's `site-theme` localStorage key, so the
  space/earth choice is shared with the wrapper page.

## Verification

- App side (Ascension workspace): schema validation + `tsc` + Vite build pass; 12 vitest
  tests pass; 7 Playwright e2e tests pass (Chrome channel), including a new 390×844 test that
  taps a node, expects the card drawer, opens the Tools drawer and closes it.
- Site side, served from this worktree with `python3 -m http.server`: full-page screenshot of
  the wrapper at 1380×900 shows nav, hero, notice, button, iframe (with the in-app banner
  visible) and the guide; at 390×844 the app shows the banner, the compact toolbar with
  Tools/Card tabs, the graph, and the node card as a bottom drawer that opens on tap and closes
  on Close.
- Not run: a check of the live GitHub Pages URL after the push (do it once Pages rebuilds);
  Lighthouse; keyboard-only navigation of the drawers.

## Left open

- Nav entry and public source when the tool stabilises.
- Whether to keep versioning the bundle here (see plan).
