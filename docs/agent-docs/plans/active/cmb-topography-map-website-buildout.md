# Plan: CMB Topography Map — website build-out

**Status:** active
**Created:** 2026-07-28
**Last revised:** 2026-07-28

## Goal

Publish and maintain an interactive, vertically-scrolling timeline of the core-mantle-boundary
(CMB) topography literature, in which every study is decoded through the same seven **ELEMENTS**
(model space, data space, model-data relation, property map, prior, output, calibration).

The page exists to make one argument visible: the forty-year CMB-topography controversy is
**not a disagreement about the Earth**, but a disagreement about which element was chosen
differently. Putting every study on one shared coordinate system is what makes that legible.

Artefact:

```
pages/research/overview/cmb/cmb-topography-map.html
css/cmb-topography-map.css
```

Plain HTML + CSS + one inline IIFE. No build step; validate in a browser.

## Design decisions

**Content provenance.** All content originates in a separate, private research repository
holding the literature map, the per-paper decodes, and the evidence-backed verification
studies. That repository is the source of truth and is *not* readable from this worktree.
Nothing on the page is authored from memory on the website side.

**Precedence.** Where a verification study exists and is closed, it supersedes the earlier
note and first-pass decode. Several dialogs therefore state what the verification study found
and then contradict the paper's own abstract. That audit voice is deliberate; preserve it.

**Publication gate.** A paper reaches the page only when its verification study is closed. Every
node currently carries the `verified` class for that reason. If the gate is ever relaxed,
unverified nodes must omit `verified` *and* the `.cmb-note` caveat must be reworded, since it
currently implies everything shown is verified.

**Evidence discipline.** Every number, page reference, sign convention and retraction on the
page traces to a closed study. An unsourced number on this page is a defect, not a rough edge.

**Confidentiality.** The upstream research material is unpublished and confidential. Only the
campaign's own analysis is published here. Long source quotations, source PDFs, internal audit
state, and upstream file paths stay out of this repository — including out of this plan.

## Scope

In scope: the timeline page, its stylesheet, its navigation entry, its search-index
registration, and the living-reference records describing them.

Out of scope: the upstream research campaign itself, and any change to how verification studies
are conducted.

### Current state

- **11 paper nodes**, all `verified`; **14 edges**; **17 reading cards**. A card is a *finding*,
  not a paper, so a heavy paper may carry two or three.
- Supporting prose: `.cmb-intro` (what the page is), `.cmb-note` (how to read it, carrying a
  `Last reviewed:` date that must be bumped on every content change), `.cmb-legend`.
- DOM order is not chronological; position is set by the hard-coded geometry below.

### Adding one paper is four coupled edits

They must stay in sync:

1. **The node button** in `#cmb-board` — the visible chip.
2. **An entry in the `details` object** in the inline script — the dialog with the seven
   ELEMENTS rows.
3. **Zero or more citation edges** — `<path class="edge …">` in the SVG.
4. **Zero or more reading cards** in `.cmb-reading`.

Plus an axis tick + label if the year is new, and band geometry if a band fills up.

---

## Layout system (read this before touching geometry)

The board is a fixed-size absolutely-positioned canvas with an SVG underlay. **All geometry is
hand-computed and hard-coded.** There is no layout engine. Get the arithmetic wrong and edges
point at nothing.

### Canvas

```
.cmb-board  { width:1200px; height:3320px }        /* css */
<svg viewBox="0 0 1200 3320">                       /* html — MUST match the css height */
```

If you extend the timeline you must change **both**.

### The three lanes (method branches)

| lane | `left` | node centre x | header |
|---|---|---|---|
| body-wave mapping | `200px` | 310 | `<text x="200" y="84">` |
| normal modes | `560px` | 670 | `<text x="560" y="84">` |
| statistical | `880px` | 990 | `<text x="880" y="84">` |

Node width is `220px` (CSS), so a lane-1 node's **right edge is x=420**, which is the anchor
every side-exiting edge uses.

### The vertical grid — the load-bearing invariant

**Row pitch is 270px.** Bands are 830px tall (3 rows) with a 30px gutter. Derived rules, all
of which hold for every existing element:

```
first row top in a band  =  band.y + 90
row tops                 =  first, first+270, first+540
axis tick y              =  row top + 77
axis label y             =  tick y + 4
band centre (for the rotated era label) = band.y + band.height/2
```

Current bands:

| class | y | height | span | era label | rows (tops) |
|---|---|---|---|---|---|
| `founding` | 110 | 830 | 110-940 | FOUNDING MAPPERS · 1986-1989 | 200, 470, 740 |
| `absorption` | 970 | 830 | 970-1800 | NORMAL MODES · 1991-1999 | 1060, 1330, 1600 |
| `probabilistic` | 1830 | 830 | 1830-2660 | THE CRITICAL TURN · 2000-2003 | 1920, 2190, 2460 |
| `critique` | 2690 | 560 | 2690-3250 | COUPLING AND SETS · 2012-2017 | 2780, 3050 |

All bands are `x="185" width="960" rx="16"`.

The era label is rotated into the left gutter deliberately — `translate(172, centre) rotate(-90)`
for the name and `translate(154, centre) rotate(-90)` for the subtitle — **so that no edge can
ever cross it**. Keep that.

Time axis: `<line class="axis" x1="110" y1="110" x2="110" y2="3260">`; ticks are
`x1="100" x2="120"`; labels `x="44"`.

### Node classes are *thematic colour*, not era

This trips people up. The four class names double as the band names but on nodes they encode
the paper's **role**, not its date:

| class | colour | meaning as used |
|---|---|---|
| `founding` | blue `#79a7da` | a body-wave mapper producing a topography map |
| `absorption` | yellow `#d9bd6c` | normal-mode / absorbed-into-a-bigger-model studies |
| `critique` | orange `#c87850` | studies that problematise the target (tradeoff, non-uniqueness, coupling) |
| `probabilistic` | purple `#bf95eb` | statistical-output studies |

`verified` is additive: it thickens the border to 2px and stamps a green **V** badge via
`::after`. **Every one of the 11 current nodes carries `verified`**, because the page's
publication gate has so far been "the verification study is CLOSED".

### Edges

```html
<path class="edge builds-on" d="…"/>   <!-- blue,   solid  -->
<path class="edge critiques" d="…"/>   <!-- orange, solid  -->
<path class="edge compares"  d="…"/>   <!-- yellow, DASHED — an analytical comparison the
                                             campaign added, NOT a real citation -->
<path class="edge applies"   d="…"/>   <!-- teal,   solid; declared in the legend and the
                                             marker defs but currently UNUSED -->
```

Arrowheads come from four `<marker>` elements in `<defs>`: `cmb-arrow-builds`,
`cmb-arrow-critiques`, `cmb-arrow-compares`, `cmb-arrow-applies`.

Anchoring conventions in use:
- **Same-lane vertical**: `M {centre} {fromTop+height} L {centre} {toTop}` — e.g.
  `M310 360 L310 462`.
- **Cross-lane**: exit the right edge (`x=420` for lane 1), run orthogonally or as a cubic,
  enter the target's centre-top. Long runs use the empty x≈470-860 corridor.

The SVG has `pointer-events:none`, so edges never intercept clicks.

### The dialog and the `details` object

`openDialog(key)` reads `details[key]` and fills `#cmb-dialog` with `title`, `sub`, `amp`,
`summary`, then iterates `elements` into a two-column grid.

**Critical constraint: it uses `textContent`, not `innerHTML`.** So in the `details` strings:

- HTML entities like `&plusmn;` will render **literally as text**. Use real characters or JS
  escapes: `\u00b1` (±), `\u211d` (ℝ), `\u00b2\u2075` (superscript 25), `\u03c3` (σ), `\u2014` (—).
- No markup. Emphasis is done with CAPITALS, which is why the existing dialogs shout
  ("the printed PKKP kernel is WRONG", "NOTHING IN THE PAPER CARRIES AN ERROR BAR").
- The `elements` object keys are the display labels and are rendered in order. Existing
  papers use exactly: `Model space`, `Data space`, `Relation`, `Property map`, `Prior`,
  `Output`, `Calibration`. **Keep those seven, in that order, for every paper.**

`amp` is the little pill (the headline amplitude). Set it to `""` for papers with no
amplitude — the code hides the pill when falsy. Several papers legitimately contribute no
amplitude (`pulliamStark1993` disclaims its own; `dahlen2005` and `russell2022` are methods
papers).

`sub` is the citation line: `Journal vol, pages · doi:…`.

### Pan/zoom

Pointer-drag to pan, wheel to zoom about the cursor, `±`/`⌖` controls, scale clamped
`[0.15, 2]`. `fitWidth()` fits the whole board on wide screens and opens phones on the year
axis plus lane 1 at a readable scale (`READ=440`). Escape closes the dialog. `userMoved`
suppresses re-fit on resize once the user has interacted. **None of this needs changing when
papers are added** — except that `fitWidth`'s wide-screen branch divides by `BOARD_W=1200`,
so if the board ever gets wider, update the `BOARD_W` constant too.

---

## Phases

### Phase 1 — Adopt and land the existing artefact ✅

The page, stylesheet, and navigation entry were built by agents working outside this
worktree's protocols and arrived as an uncommitted working tree. Phase 1 reconciled that work
with the local systems and landed it.

Record: `docs/agent-docs/plans/completed/cmb-topography-map-website-buildout-phase-1-complete.md`

**Next phase: 2.**

### Phase 2 — Board recompute and a geometry generator

**Do this before adding any queued paper.** Inserting papers mid-timeline invalidates every
downstream coordinate. The queued backlog on a 270px pitch is roughly 3500px of new board, and
most of it inserts *before* existing nodes. A naive insert breaks node `top`s, all 12 axis
ticks and labels, all 4 band rectangles, all 4 rotated era labels, the axis endpoint, the board
height in two files, and all 14 edge paths.

Two approaches were considered:

- **(A) Recompute the whole board.** Fix the final paper set and era bands, lay out every row
  on the 270px pitch, then regenerate ticks, bands, labels and edges from the derived rules
  above. One big diff, done in a single pass.
- **(B) Use all three lanes per row.** Rows currently hold one node even though three lanes
  exist. Contemporaneous papers from different branches should share a row. This keeps the
  board shorter and is truer to the data.

**Decision: (B) within (A).** One full recompute, using all three lanes per row. Consider
resizing era bands to hold more than three rows, since the early 1990s and the 2000s are dense.

Write a small offline generator (Python, emitting the SVG block and node buttons from a table
of `citekey, year, lane, class`) to remove the arithmetic risk. `figure_generation/` is the
precedent for offline tooling that is not served and carries its own pytest suite.

### Phase 3 — Publish the queued backlog

Papers whose verification studies are closed but which are not yet on the page. Findings,
amplitudes and evidence stay in the upstream research repository and are written into the
dialogs at the time each node is added, per the procedure below.

| citekey | year | lane | class |
|---|---|---|---|
| `gudmundssonClayton1991` | 1991 | statistical | `critique` |
| `emmerich1993` | 1993 | body-wave | `critique` |
| `pulliamStark1993` | 1993 | statistical | `critique` |
| `rodgersWahr1993` | 1993 | statistical | `critique` |
| `starkHengartner1993` | 1993 | statistical | `probabilistic` |
| `trampert2004probabilistic` | 2004 | statistical | `probabilistic` |
| `dahlen2005` | 2005 | body-wave | `critique` |
| `tanaka2010` | 2010 | body-wave | `founding` |
| `moscaCobden2012` | 2012 | statistical | `probabilistic` |
| `colombi2014` | 2014 | body-wave | `critique` |
| `moulikEkstrom2016` | 2016 | normal modes | `absorption` |
| `muir2022` | 2022 | body-wave | `probabilistic` |

Suggested ordering once Phase 2 lands:

1. **`tanaka2010` first.** The page already narrates an amplitude collapse across two reading
   cards but stops one rung short, so it currently under-tells its own best story.
2. **Then the 1993 papers as one three-lane row**, which establishes the multi-column pattern
   and fills the era band that exists partly in anticipation of them.

`russell2022` is deliberately excluded from the table. It instantiates none of the seven
elements — it sits upstream of the data space — so it belongs as a footnote or aside rather
than a timeline node. Decide its treatment in Phase 4.

Papers whose verification is still open are out of scope while the publication gate holds.

### Phase 4 — Output and calibration visualisation

The strongest untold result is that one physical target has produced many distinct output
types across several calibration states. The page has no visualisation of this. A compact
output/calibration table, or a colour-coded output badge on each node, would land the argument
harder than any additional node.

Also in this phase:

- **Resolve the `applies` edge type.** It is declared in the legend, the CSS and the marker
  defs but never used. Either use it or remove it from the legend.
- **Decide the `russell2022` treatment** as a footnote or aside.

---

## Procedure for adding one paper

1. **Read the paper's verification study** in the upstream research repository, including its
   retraction log, and cross-read the corresponding decode. Write the dialog from the
   *corrected* position, not the first pass.
2. **Confirm the study is closed.** If it is still open, do not add the node with a `verified`
   badge.
3. **Write the `details` entry** — `title`, `sub` (journal + doi), `amp`, `summary`, and the
   seven `elements` rows. Unicode escapes only, no HTML entities, no markup.
4. **Place the node** — lane by branch, class by role, `top` on the 270px pitch. Add the axis
   tick and label if the year is new.
5. **Draw edges** — only relationships that can be defended. `builds-on` for real citation
   lineage, `critiques` for a critique, `compares` (dashed) for an analytical comparison drawn
   by the campaign rather than a citation. Do not invent citations.
6. **Add a reading card** for each genuinely quotable finding. Two or three per heavy paper is
   normal.
7. **Bump `Last reviewed:`** in `.cmb-note`.
8. **Bump the `?v=N` cache-bust** on `cmb-topography-map.css` if the CSS changed (site-wide
   search-replace per `AGENTS.md`; currently `v=38`).
9. **Rebuild the search index** with `python3 tools/build_search_index.py` and commit the
   refreshed `media/search-index.json` with the content change. The `cmb/` directory is
   registered in `tools/build_search_index.py`; a new page in that directory is picked up
   automatically, but a page added elsewhere must be registered first.
10. **Verify in a browser.** Check that no edge points at empty space, click every new node,
    confirm no dialog renders a literal `&plusmn;`, and check the layout at ~400px.
11. **Commit** per `docs/agent-docs/COMMIT_CONVENTION.md` with a `Plan:` trailer referencing
    this file.

---

## Environment and gotchas

- **Two repositories.** The research content lives in a separate private worktree that this
  repository cannot read. Content must be carried across deliberately; it cannot be looked up
  mid-edit from here.
- **Local preview.** `python3 -m http.server 8765` from the repository root, then open
  `/pages/research/overview/cmb/cmb-topography-map.html`. Check for a stale server on that port
  before starting a new one.
- **Nav is duplicated in every page.** The CMB entry is present in every dropdown that carries
  the `Notes` section. Two harness pages (`agentic-structure-map.html`,
  `workspace-explorer.html`) deliberately use a shortened dropdown with no `Notes` section and
  correctly omit it. Any future nav change must still be applied site-wide.
- **Privacy.** The upstream material is confidential unpublished work whose studies quote
  source PDFs page by page. Publish only the campaign's own analysis. Do not transcribe long
  source quotations, and never copy upstream text, source PDFs, or internal audit state into
  this repository — this plan included.
- **Do not weaken the audit voice.** Several dialogs contradict published abstracts on the
  record. That is the page's value. Every such statement must trace to a closed study.

---

## Open questions

- **Era-band capacity.** Should bands be resized to hold more than three rows before the
  Phase 2 recompute, given the density of the early 1990s and the 2000s?
- **Generator scope.** Should the Phase 2 generator emit the whole board (bands, ticks, era
  labels, nodes, edges), or only the error-prone node/tick/band geometry, leaving edges
  hand-drawn?
- **`russell2022` placement.** Footnote, aside, or an off-timeline upstream marker?
- **Dialog text is not searchable.** The `details` content lives in an inline `<script>`, which
  the search-index builder skips by design. The richest text on the page — the ELEMENTS decode
  for each paper — is therefore not findable via site search. Accept, or move the data into
  markup?
