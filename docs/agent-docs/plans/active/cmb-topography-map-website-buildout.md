# Plan: CMB Topography Map — website build-out

**Status:** active
**Created:** 2026-07-28
**Last revised:** 2026-08-03

> **Publication status (2026-08-03): withheld from the live site.** The map was
> taken offline in commit `0ccf7da` because the timeline is not yet complete. The
> page and stylesheet remain in the repository but are excluded from the GitHub
> Pages build (`_config.yml`); all nav links, the research-overview index card,
> and the search-index entry were removed. To republish: undo the two
> `_config.yml` exclude lines, restore the links/card/search-builder entry, and
> rebuild the search index. The Goal below still describes the intended
> published end state.

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
studies. That repository is the source of truth, and it **is readable from this machine** —
the local control overlay records where. Read the relevant verification study directly rather
than working from a summary; nothing on the page is authored from memory on the website side.

The study index is the authority for which papers are closed. Re-read it at the start of any
phase-3 work rather than trusting a count written into a plan, because studies close over
time and any count here goes stale.

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

- **23 paper nodes**, all `verified`; **27 edges** (14 original + 13 new from Phase 3);
  **29 reading cards** (17 original + 12 new from Phase 3). A card is a *finding*, not a paper,
  so a heavy paper may carry two or three.
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
.cmb-board  { width:1200px; height:5480px }        /* css */
<svg viewBox="0 0 1200 5480">                       /* html — MUST match the css height */
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

**Row pitch is 270px.** Bands vary in height by row count (270×N + 20) with a 30px gutter.
Derived rules, all of which hold for every element:

```
first row top in a band  =  band.y + 90
row tops                 =  first, first+270, first+540, ...
axis tick y              =  row top + 77
axis label y             =  tick y + 4
band centre (for the rotated era label) = band.y + band.height/2
```

Current bands (after Phase 2 recompute):

| class | y | height | span | era label | rows |
|---|---|---|---|---|---|
| `founding` | 110 | 830 | 110-940 | FOUNDING MAPPERS · 1986-1989 | 200, 470, 740 |
| `absorption` | 970 | 1640 | 970-2610 | NORMAL MODES AND CRITIQUES · 1991-1999 | 1060, 1330, 1600, 1870, 2140, 2410 |
| `probabilistic` | 2640 | 1100 | 2640-3740 | THE CRITICAL TURN · 2000-2005 | 2730, 3000, 3270, 3540 |
| `critique` | 3770 | 1640 | 3770-5410 | COUPLING AND POSTERIORS · 2010-2022 | 3860, 4130, 4400, 4670, 4940, 5210 |

All bands are `x="185" width="960" rx="16"`.

The era label is rotated into the left gutter deliberately — `translate(172, centre) rotate(-90)`
for the name and `translate(154, centre) rotate(-90)` for the subtitle — **so that no edge can
ever cross it**. Keep that.

Time axis: `<line class="axis" x1="110" y1="110" x2="110" y2="5420">`; ticks are
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
`::after`. **All 23 current nodes carry `verified`**, because the page's
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

**Next phase: 3.**

### Phase 2 — Board recompute and a geometry generator ✅

**Completed.** The board was recomputed from 11 papers / 11 rows / 3320px to 23 papers / 19
rows / 5480px. All three lanes are now used per row where papers are contemporaneous. Era
bands were resized: the 1991-1999 band holds 6 rows, the 2000-2005 band holds 4 rows, and the
2010-2022 band holds 6 rows.

The offline generator lives at `tools/cmb_geometry_generator.py` (stdlib only). It emits the
SVG block (defs, lane headers, era bands, era labels, time axis, ticks, labels) and the HTML
node buttons from a paper layout table. Edges are hand-drawn against the computed coordinates
and updated in the same pass.

The 12 newly placed nodes have no `details` entries yet — Phase 3 will add those, along with
reading cards and new citation edges.

### Phase 3 — Populate the queued nodes ✅

**Completed.** All 12 newly placed nodes now have `details` entries (7 ELEMENTS rows each),
reading cards, and citation edges. The page carries 23 nodes, 27 edges, and 29 reading cards.
CSS cache bumped to v=41; search index rebuilt; `Last reviewed` updated to 29 July 2026.

The 12 papers populated:

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

`russell2022` is deliberately excluded. It instantiates none of the seven elements — it sits
upstream of the data space — so it belongs as a footnote or aside rather than a timeline node.
Decide its treatment in Phase 4.

`lau2017tidal` is placed as an off-timeline aside (`cmb-aside`) with a
reading card, not as a timeline node. Its data space is non-seismic (M2 body
tide at 456 GPS stations), so it fits none of the three lanes, and its CMB
result is negative (matched-filter SNR 0.03–0.10). The aside explains the unique
set-output / none-exercised cell it occupies and why it sits off-timeline.

Papers whose verification is still open are out of scope while the publication gate holds.

**Next phase: 4.**

### Phase 4 — Output and calibration visualisation ✅

**Completed.** A calibration badge (coloured dot) was added to every node: grey for
none, blue for frequentist, orange for deterministic, purple for Bayesian. The
legend now carries four calibration keys alongside the existing edge and
verified keys. An output/calibration summary table below the map lists all 23
papers with their output type, calibration state, and headline amplitude.

The `applies` edge type was removed from the legend, the CSS, and the SVG marker
defs — no paper in the corpus uses it.

`russell2022` was placed as an aside (`cmb-aside`) above the summary table, not
as a timeline node, because it instantiates none of the seven ELEMENTS.

CSS cache bumped to v=42; search index rebuilt; `Last reviewed` updated.

**Remaining open questions:**

- Dialog text is not searchable (inline `<script>` skipped by the index builder).

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
   search-replace per `AGENTS.md`; currently `v=42`).
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

- **Era-band capacity.** Resolved in Phase 2: bands now hold 3/6/4/6 rows respectively.
- **Generator scope.** Resolved in Phase 2: the generator emits bands, ticks, era labels, and
  nodes. Edges are hand-drawn against the computed coordinates.
- **`russell2022` placement.** Footnote, aside, or an off-timeline upstream marker?
- **Dialog text is not searchable.** The `details` content lives in an inline `<script>`, which
  the search-index builder skips by design. The richest text on the page — the ELEMENTS decode
  for each paper — is therefore not findable via site search. Accept, or move the data into
  markup?
