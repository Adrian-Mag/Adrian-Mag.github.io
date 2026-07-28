# Phase 1 complete — CMB Topography Map: adopt and land the existing artefact

**Plan:** `docs/agent-docs/plans/active/cmb-topography-map-website-buildout.md`
**Phase:** 1 of 4
**Completed:** 2026-07-28
**Base commit at start:** `8c129a6`

## Context

The CMB Topography Map page, its stylesheet, its site-wide navigation entry, and its plan
document were produced by agents working outside this worktree, with no knowledge of the local
control overlay, the plans protocol, the living-reference contract, or the search-index
builder. The work arrived as an uncommitted working tree: two untracked files, one untracked
plan, and 72 modified HTML files.

The artefact itself was judged sound. Phase 1 was therefore **protocol reconciliation, not
authoring**: make the existing work comply with the workspace's systems and land it.

## What was done

### Control recovery

The control applicability check failed on entry:

```
FAIL: handoff does not apply to this worktree:
tracked_worktree_clean: recorded=True, actual=False
```

`HANDOFF.json` and `CURRENT.md` were rebuilt from Git evidence rather than trusted, per the
recovery route. Branch and HEAD were unchanged; only the dirty-state claim was stale. The
validator passed on recheck.

### Dirty-tree provenance audit

The inherited plan asserted that the dirty tree was an unrelated "site-wide cache-bust/nav
sweep in flight" that had to be reconciled before starting. **That was wrong**, and acting on
it would have caused an attempt to separate or revert work that belonged to this feature.

The actual diff over all 72 modified HTML files contained only:

- one `CMB Topography Map` entry added to each `nav-drop-menu`;
- one research card added to `pages/research/overview/index.html`;
- a rebuilt `media/search-index.json`;
- four additions to the living website reference.

No unrelated changes, and no cache-bust edits. All of it is one feature and was landed as one
unit.

### Defect found and fixed: the page could never be indexed

`media/search-index.json` was modified, which gave the appearance that the search index had
been rebuilt for the new page. It had not been. The page was absent from the index; the file
differed only because nav text is indexed and the nav had changed on 72 pages.

Root cause: `tools/build_search_index.py` walks an **explicit allowlist**, not the pages tree.
`pages/research/overview/cmb` was never registered, so no number of rebuilds could have
included the page.

Fix: registered the directory in `SERIES_DIRS` with the series label `CMB Topography Studies`,
so the current page and any future page in that directory are indexed automatically.

### Verified-intentional, not fixed

73 pages carry a `nav-drop-menu`; 71 gained the CMB link. The two exceptions,
`pages/research/overview/harness/agentic-structure-map.html` and
`pages/research/overview/workspace-explorer.html`, deliberately use a shortened dropdown that
ends at `The Machine Around the Model` and carries no `Notes` section or any other note-series
link. Omitting the CMB entry there is correct; no change was made.

### Plan restructured and sanitised

The inherited document was a session handoff narrative, not a plan under
`docs/agent-docs/plans/PROTOCOL.md`. It was restructured to the required shape (Goal, Design
decisions, Scope, Phases, Open questions) with four phases, preserving the genuinely valuable
content: the hard-coded board geometry rules, the lane and band tables, the `textContent`
constraint on dialog strings, and the per-paper procedure.

`docs/agent-docs/plans/` is tracked and public. The inherited text would have published private
machine paths, upstream repository file paths, internal audit state (which studies are closed
or open, study numbers, hypothesis numbering), and unpublished findings for twelve papers not
yet on the page. On the user's decision, the plan was sanitised: machine paths removed, the
upstream repository referred to abstractly, and the backlog reduced to citekey, year, lane and
class with no findings text. The findings remain in the upstream research repository, which is
where they belong until the user chooses to publish each node.

## Decisions that became settled

- The artefact is accepted on its merits; Phase 1 does not re-author page content.
- The upstream research repository is the source of truth for all page content and is not
  readable from this worktree. Content is carried across deliberately, never looked up
  mid-edit.
- The public plan carries no upstream findings, paths, or audit state. Publication of each
  paper's findings happens when its node is added, under the user's editorial control.
- The `cmb/` directory is a registered search-index series, so future pages there are indexed
  without touching the builder.
- Phase 2 (board recompute plus a geometry generator) must precede any queued paper. The
  hand-computed geometry makes incremental mid-timeline insertion the dominant risk.

## Verification

| Check | Result |
|---|---|
| Control applicability (`controlctl.py begin`) | Failed on entry; passed after rebuilding `HANDOFF.json` and `CURRENT.md` from Git evidence |
| Dirty-tree provenance audit | Passed — all 72 modified files contain only the CMB nav line; no unrelated work mixed in |
| Artefact structural spot-check | Passed — 11 unique `data-node` keys, 14 edge paths, 17 reading cards; `viewBox="0 0 1200 3320"` matches `.cmb-board` width/height in CSS; stylesheet at `?v=38` |
| HTML parse | Passed |
| Inline JavaScript syntax | Passed — both inline blocks clean under `node --check` |
| Nav coverage | Passed — 71 of 73 dropdown pages carry the link; the 2 exceptions verified as intentionally shortened navs |
| Search-index registration | Failed, then fixed — page absent from the index; builder allowlist updated; rebuild now indexes 63 pages with the page present |
| Living-reference coverage | Passed — `cmb/` tree entry, CSS mapping, path rule and page-role row all already present |
| Sensitive-string sweep (page) | Passed — no machine paths, upstream paths, IPs, keys or contact details |
| Sensitive-string sweep (plan) | Failed, then fixed — private machine paths and upstream audit state removed during the sanitisation |

## Verification not run

- **Browser and mobile rendering.** Not executed in this phase. The page was not modified, so
  its rendering is unchanged from the state the authoring agents left it in, but no independent
  desktop or ~400px check was performed here. The Python Playwright binding is broken in this
  repository and Node Playwright is not installed; use headless Chrome.
- **Edge-anchor inspection.** Not re-derived. The 14 edge paths were counted but their
  coordinates were not checked against node positions. Phase 2 will regenerate them.
- **Upstream claim re-verification.** Impossible from this worktree by design. The page's
  factual claims rest on the upstream verification studies and were not re-checked here.

## Follow-ups

- Phase 2 board recompute and geometry generator, before any queued paper is added.
- ~~Run a browser and narrow-viewport check on the page at the next opportunity.~~ Done; see
  the addendum below.
- Consider whether the dialog `details` data should move into markup so the richest text on the
  page becomes searchable; recorded as an open question in the plan.

---

## Addendum — 2026-07-28: deferred browser check run, one bug found and fixed

Playwright was repaired after this phase was committed. The diagnosis carried in the control
handoff — that the Python binding failed before launch — was wrong. The binding and Node driver
worked; the browser binaries had simply never been downloaded
(`playwright install chromium`, Chromium 130.0.6723.31). No version change was needed, and the
Playwright 1.48 pin was left alone because it is one of the last releases supporting this
Ubuntu 20.04 / glibc 2.31 host.

The deferred check was then run and found a genuine interaction bug.

**Bug.** `.cmb-status` and `.cmb-flow` are non-interactive text labels positioned over the
board at `z-index:3`, while `.cmb-node` chips sit at `z-index:2`. Neither label set
`pointer-events:none`, so any node panned underneath the zoom readout or the flow label became
unclickable — the label swallowed the click. The SVG edge layer already guarded against exactly
this on line 21 of the stylesheet; these two labels were missed.

Playwright surfaced it by exhausting 60+ retries on one node with
`<p id="cmb-status"> intercepts pointer events`.

**Fix.** Added `pointer-events:none` to both rules in `css/cmb-topography-map.css`, and bumped
the stylesheet cache version from `?v=38` to `?v=39`. `.cmb-controls` deliberately keeps its
pointer events because its buttons are real controls.

**Verification after the fix**, at 1440x900 and 390x844:

| Check | Result |
|---|---|
| Nodes found | 11 |
| Clicks blocked | none |
| Dialogs empty after click | none |
| Literal unrendered entities in dialogs | none |
| Console errors | none |
| Uncaught page errors | none |
| Horizontal overflow at 390px | none (`scrollWidth` 390 = `innerWidth` 390) |

Every one of the 11 nodes was clicked and its dialog inspected, which also confirms the
`details` object has no missing or misspelled keys.

**Still not verified.** Edge-path coordinates were counted but never re-derived against node
positions; Phase 2 will regenerate them. The page's factual claims still rest on the upstream
verification studies and cannot be re-checked from this worktree.
