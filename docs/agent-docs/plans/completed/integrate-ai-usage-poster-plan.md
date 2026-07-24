## Plan: Integrate the "AI Usage" Poster into the Website

**Status:** completed   **Created:** 2026-07-10   **Archived:** 2026-07-22

### Goal

A finished artifact — `pages/research/posters/ai-usage-poster/ai-usage-poster.html` —
needs to be wired into the live site. It is a self-contained, evidence-backed poster
arguing that Adrian's AI usage in research is rigorous engineering, not "AI slop",
aimed specifically at researchers who are skeptical of AI in academic work (people who
only know ChatGPT-style copy-paste use and assume anything more is either hype or
cheating). This plan hands the integration work to whichever agent picks it up next; the
content itself was built and privacy-reviewed in a separate workspace (the PhD thesis
repo) and should not need further editing, only wiring into navigation/discovery.

### What the poster is

A single HTML page (2.5 MB, everything embedded as inline data — no external requests,
no dependencies, opens offline in any browser) that argues its case in three layers:

1. **A myth-vs-mechanism strip** — four things a skeptic believes about AI usage,
   each answered with a concrete *mechanism* rather than a reassurance (e.g. "the
   model is forbidden to assert mathematics from memory" rather than "trust me, it's
   careful").
2. **Six pillars** — source-grounded verification, privacy-by-mechanism (a hook that
   mechanically blocks network access to unpublished work), plans wired into git
   history, autonomous compute missions on a personal server, an adversarial
   manuscript-review pipeline, and graph-based literature mapping.
3. **"The receipts"** — nine exhibits, each a genuine artifact screenshotted from real
   files/logs on Adrian's machine (not mocked up), captioned with what it proves.

### How it was made (for provenance / so the next agent isn't guessing)

Built inside `~/PhD/thesis` across several turns with Claude Code:

- The prose was drafted, then corrected twice by the user (role: theoretical/
  computational geophysicist, not mathematician; "europa" = a personal office PC
  turned into a private compute server, not an institutional HPC; generic "work" /
  "scientific work" instead of naming "thesis" or "paper" anywhere in the copy).
- The nine exhibits were extracted directly from live systems, not fabricated:
  - **Exhibit 1** — a citation-verification note plus cropped pages of the actual
    cited textbook (Kreyszig), rendered from a local PDF library via
    `pdf-source-reading` tooling.
  - **Exhibit 2** — a genuine privacy-guard denial event, pulled from a past Claude
    Code session transcript (`~/.claude/projects/.../*.jsonl`) by grepping for the
    hook's real denial string and extracting the surrounding tool-call/tool-result
    pair. **The real IP address of the personal server was redacted** before
    publication (see Privacy review below).
  - **Exhibit 3** — the literal first lines of a Scout-mode query-audit log
    (DOIs/titles only, the one sanctioned online channel).
  - **Exhibit 4** — a real planning document from a separate research-software repo.
  - **Exhibit 5** — originally a `latexdiff` page showing an unpublished paper's
    math; **replaced** before publication with a genuine software bug-fix diff
    instead (see Privacy review).
  - **Exhibit 6** — a real long-running-mission brief (seismology kernel validation
    against published reference papers).
  - **Exhibit 7** — a real `.europa.yml` sync config for the personal compute server.
  - **Exhibit 8** — originally a thesis literature note; **replaced** with a note
    from a second, independent literature-mapping project instead, so the exhibit
    isn't thesis-specific (see Privacy review).
  - **Exhibit 9** — a citation graph auto-rendered from structured literature-note
    edges (Graphviz), not hand-drawn.
- All nine embedded images were verified byte-for-byte against their source PNGs
  after a real bug surfaced: 7 of 9 were found silently corrupted (undecodable,
  rendering as blank boxes) partway through editing, almost certainly from some
  external text-processing pass mangling raw base64 as if it were prose. All were
  re-embedded and re-verified; the current file passes a full decode+byte-match
  check on every exhibit.

### Privacy review already completed (do not re-litigate without the user)

Two items were explicitly flagged to the user and resolved before this file was
finalized:

1. **Exhibit 2's IP address** — europa's real IP appeared in a terminal transcript.
   User chose: redact. Done (shown as a solid redaction bar in the image).
2. **Exhibit 5's content** — originally showed real, unpublished equations/results
   from an active paper (a new Result + Corollary, pre-submission). User chose:
   swap to a non-scientific example. Done — it now shows a real software bug fix
   (`intervalinf/.../posterior_viz.py`, an `else` → `elif len(...) > 0` crash fix)
   with zero scientific content.

Everything else in the nine exhibits was reviewed and judged safe to publish: no
novel scientific claims, no unpublished results, no credentials. Two categories are
worth the next agent/human's own eyes regardless: Exhibit 1 quotes one sentence from
the thesis's own verification notes (about a standard textbook theorem, not a novel
claim), and Exhibit 9's citation graph reveals the *scope* of the thesis literature
review (topics/structure, not results). Both were judged low-risk, not zero-risk —
flagging them here so a human can veto before the first push if they disagree.

### Files / components delivered

```
pages/research/posters/ai-usage-poster/ai-usage-poster.html   the poster (self-contained)
media/research/posters/thumbnails/ai-usage-poster.png         candidate thumbnail (400x226,
                                                                cropped from the poster's own
                                                                header — swap freely if a
                                                                better crop is wanted)
```

The `posters.html` grid was not touched. The poster is now linked directly from
the Research dropdown on all 48 HTML pages with the nav, under "Presentations",
labelled "AI-Assisted Research". No CSS file was modified.

### Phases

1. **Phase 0 (done, this handoff)** — asset + thumbnail placed, this plan written.
2. **Phase 1 (done)** — User decided: the page is **not** a poster card in the
   grid. It is a standalone page linked directly from the site-wide Research
   dropdown, under "Presentations", labelled "AI-Assisted Research". The poster
   file stays at its current path (`pages/research/posters/ai-usage-poster/`)
   but is linked from the nav dropdown on all 48 HTML pages with the dropdown.
3. **Phase 2 (done)** — Added `<a href="...">AI-Assisted Research</a>` to the
   `dropdown-content` after "Presentations" on all 48 pages, with correct
   relative paths per directory depth.
4. **Phase 3 (complete)** — Static status check on 2026-07-22 confirmed the
   poster title, `main`, and footer landmarks; all 21 local page assets; and
   all 71 current site links labelled “AI-Assisted Research” resolve to the
   poster. This records the available verification without claiming a new
   browser run.
5. **Phase 4 (complete)** — The delivered poster and its navigation wiring are
   already in Git history (`997ce93`, with later poster refinements). The user
   confirmed the page is done; this plan is therefore archived without a new
   product commit.

### Optional follow-up ideas (not part of this completed plan)

- **Standalone vs. reskinned:** the poster currently has its own header/footer and
  does *not* share the site's `<nav>`/`styles.css` (unlike `BSM24.html`, which is
  reskinned into the site chrome). Keeping it standalone is zero-risk and preserves
  the artifact exactly as reviewed; reskinning it into the site's nav/CSS is more
  consistent with the rest of the site but is new work and a new review surface.
  Recommend: ship standalone first, reskin later only if asked. Whatever is chosen,
  avoid modifying the file at
  `pages/research/posters/ai-usage-poster/ai-usage-poster.html` in place; if a
  reskinned variant is wanted, do so as an explicit, reviewable change afterward.
- **Thumbnail:** the shipped one is a quick header crop, functional but plain. Not
  needed for the dropdown link (no thumbnail shown there), but could be useful if
  the page is ever referenced from a card grid. Not blocking.

### Closing note

The standalone poster remains the approved final form. The reskin and thumbnail
ideas are optional future work, not open requirements for this delivery.
