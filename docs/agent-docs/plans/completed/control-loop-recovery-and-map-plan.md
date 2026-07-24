# Control loop recovery and anatomy map

**Status:** complete
**Created:** 2026-07-22
**Scope:** local control overlay (never staged) and the public workspace anatomy map

## Goal

Turn the local `website-control` routine into an honest closed work loop: a failed
applicability check stops workspace work, records a redacted local incident, is
repaired from source and Git evidence, and must pass again before work resumes.
Replace the public lifecycle map with an original hardware-inspired anatomy map
that makes this route, its limits, and the surrounding context/actions/persist/
verification parts visible.

## Decisions

- The control overlay remains local-only. Incident details are not served,
  staged, committed, or copied into public documentation.
- A failed applicability check blocks workspace work except the diagnosis needed
  to rebuild the notes. The validator records only redacted categories, keeps
  the newest 100 event records, and maintains durable monthly/category totals.
- The public diagram describes the system as it exists: the workspace workflow
  is soft control, the host conversation loop is not a workspace rule, and
  optional abilities are not automatic workflows.
- The diagram replaces `agentic-structure-map.html` and uses an original SVG
  board with pan/zoom and short node explanations. Essential route steps remain
  visible on the board rather than being hidden in a popup.

## Phase 1 — close the local control loop

**Status:** complete

- [x] Add the local, redacted incident ledger and summary to the manifest and validator.
- [x] Make validator failure categories actionable without recording raw Git or path values.
- [x] Make startup, recovery, plan-routing, phase landing, and close/revalidate
      rules explicit in the skill and maintenance guide.
- [x] Refresh local orientation and handoff after a passing control check.

## Phase 2 — build the public anatomy map

**Status:** complete

- [x] Replace the lifecycle map with the hardware-inspired interactive board.
- [x] Show the full control loop, including recovery, plan choice, phase landing,
      close, and the next-prompt boundary.
- [x] Explain context injection, action tools, persistent records, verification,
      automatic checks, optional abilities, and known gaps in plain language.
- [x] Update the series plan/source dossier only where local-control exhibits or
      measurements have changed.

## Phase 3 — verify and hand off

**Status:** complete

- [x] Run control-structure and incident-ledger checks without polluting the
      live incident history.
- [x] Rebuild the search index after served prose edits.
- [x] Check HTML structure.
- [x] Inspect the interactive map in Playwright at desktop and narrow widths.
- [x] Update this plan, the required phase-completion record(s), `CURRENT.md`,
      and `HANDOFF.json` with the actual result.

Playwright Chromium now provides the focused browser check. It found and guided
the repair of two node-overlap pairs, initial framing that clipped the control
region, floating connector paths, and a drag-handler conflict that swallowed
zoom-control clicks. The final desktop and narrow checks found no overlap or
viewport overflow; all mapped nodes fit their intended regions; a popup,
zoom, and reset all worked.

## Affected files

- Local-only: `docs/agent-docs/control/CONTROL.json`, `CURRENT.md`,
  `HANDOFF.json`, `MAINTENANCE.md`, `skills/website-control/SKILL.md`, and
  `scripts/validate_control.py`, plus the local incident records.
- Tracked: `AGENTS.md`,
  `pages/research/overview/harness/agentic-structure-map.html`,
  `media/search-index.json`, the Machine Around the Model plan/source dossier,
  and phase-completion records.

## Open questions

- Whether recurring real incident totals eventually justify changing the control
  design remains an evidence-led future decision, not an automatic escalation.
