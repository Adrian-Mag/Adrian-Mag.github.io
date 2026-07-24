## Control loop recovery and anatomy map — Phase 3 complete

**Plan:** `docs/agent-docs/plans/completed/control-loop-recovery-and-map-plan.md`
**Completed:** 2026-07-22

### Done

- Ran the dedicated local Playwright Chromium audit at desktop and narrow widths.
- Repositioned overlapping nodes, expanded the action enclosure, and reset the
  initial board framing so the entire control enclosure is visible on desktop.
- Rewired every visible connector to a source and destination node or region.
- Fixed the drag handler so it does not capture clicks intended for zoom controls.

### Verification

- Playwright found no node overlap, no node outside its intended enclosure, and
  no document-width overflow at 1440px or 390px.
- A context-node popup, zoom control, and reset control all worked in Playwright.
- HTML parsing, search-index rebuild, control validation, and whitespace check passed.

### Deviations

None.
