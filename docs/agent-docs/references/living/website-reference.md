# Website Living Reference

## Scope

This document describes the structure, conventions, and file mappings for the
`Adrian-Mag.github.io` static website. Read this before modifying any page or
stylesheet. Update this file whenever pages, CSS files, or navigation links are
added, removed, or restructured.

---

## Site Architecture

The site is **plain HTML5 + CSS3** with no build step, no JavaScript framework,
and no preprocessor. All pages are served directly by GitHub Pages. A small amount
of vanilla JS is used for interactive features (concept popups, Plotly panel,
scroll-spy navigation).

### Directory Layout

```
index.html                          # Home page (root)
output.html                         # (legacy/scratch output page)
css/                                # All stylesheets
js/                                 # JavaScript (concept-popup.js, refinement-panel.js)
pages/
    about.html
    contacts.html
    cv.html
    research/
        overview/                  # Research overview + theory topics
            index.html               # (was research_overview.html)
            inversions-inferences.html
            ai-in-practice.html          # Landing for AI-related notes and teaching material
            bayes/                       # Bayes, Measure-Theoretically (landing + multi-page parts)
                bayes-measure-theoretically.html
                part-1.html
                part-2.html
                part-3.html
                part-3a.html
                part-3b.html
                part-3c.html
                part-3d.html
                part-3e.html
                part-3f.html
                part-4.html
            frequentist/                 # Bayesian and Frequentist Inference (landing + multi-page parts)
                bayesian-frequentist.html
                part-1.html
                part-2.html
                part-3.html
                part-4.html
                part-5.html
            think-first/              # Think First, Discretize Later (landing + multi-page acts)
                think-first-discretize-later.html
                act-1.html
                act-2.html
                act-3.html
                act-4.html
                act-5.html
                act-6.html
                act-7.html
                act-8.html
                summary.html
            sola/                        # My Take on SOLA (landing + multi-page acts)
                my-take-on-sola.html
                act-1.html
                act-2.html
                act-3.html
                act-4.html
                act-5.html
                act-6.html
                act-7.html
                act-8.html
                act-9.html
                act-10.html
                act-11.html
                summary.html
            harness/                     # The Machine Around the Model (landing + 11 acts)
                the-machine-around-the-model.html
                act-1.html ... act-11.html
                agentic-structure-map.html # interactive workspace-control map
                workspace-explorer.html    # recursive VS Code-style agent-infrastructure tree
                summary.html
            cmb/                        # CMB Topography Studies (interactive timeline)
                cmb-topography-map.html
        publications/
            papers.html
        posters/
            posters.html
            BSM24/
                BSM24.html
media/
    Long_CV.pdf                     # Sanitised, evidence-linked public CV download
    earth_interior.png
    backgrounds/                    # Full-bleed hero background images
        cygnus.jpg
        pleiades_medium.jpg
        triangulum.jpg
        vertical.jpg
    personal/                       # Personal photos
    research/
        posters/
            BSM24/                  # BSM24 poster PDF assets
            thumbnails/             # Poster preview thumbnails
        think-first/                # Think First, Discretize Later figures + JSON
docs/
    agent-docs/
        COMMIT_CONVENTION.md       # Commit-message format and plan traceability
        PROTOCOL.md                # Cross-protocol map for agent documentation
        plans/
            PROTOCOL.md            # Plan lifecycle rules
            active/                # Current, durable plans
            completed/             # Completed and archived plan records
        references/
            PROTOCOL.md            # Reference lifecycle rules
            INDEX.md               # Need-to-record registry
            living/
                website-reference.md   # ← this file
                agent-docs-reference.md # Agent-document protocol map
            sources/               # Claim and artifact evidence dossiers
        citation-audit/            # Private local citation-evidence protocol + library
        agent-ledger/              # Soft procedure-observation protocol
        control/                   # Ignored local continuity state and canonical workflow
figure_generation/                  # Python scripts for generating page figures (conda env: inferences)
    think_first_discretize_later/   # Figures + interactive data for the Think First page
```

---

## CSS Conventions

### Stylesheet Pairing

Every page loads **two CSS files**:
1. `css/styles.css` — site-wide shared styles (typography, nav, header, footer, reset)
2. A page-specific stylesheet named after the page, e.g.:
   - `index.html` → `css/index.css`
   - `pages/about.html` → `css/about.css`
   - `pages/cv.html` → `css/cv.css`
   - `pages/contacts.html` → `css/contacts.css`
   - `pages/research/overview/index.html` → `css/research_overview.css` (three levels up: `../../../css/`)
   - `pages/research/overview/inversions-inferences.html` → *(no dedicated stylesheet)*
   - `pages/research/overview/ai-in-practice.html` → `css/harness.css` (three levels up: `../../../css/`)
   - `pages/research/overview/bayes/bayes-measure-theoretically.html` → `css/bayes-measure-theoretically.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/bayes/part-*.html` → `css/bayes-measure-theoretically.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/think-first/think-first-discretize-later.html` → `css/think-first-discretize-later.css` + `css/concept-popup.css` + `css/refinement-panel.css`
   - `pages/research/overview/think-first/act-*.html` → `css/think-first-discretize-later.css` + `css/concept-popup.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/think-first/summary.html` → same as act pages
   - `pages/research/overview/frequentist/bayesian-frequentist.html` → `css/frequentist.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/frequentist/part-*.html` → `css/frequentist.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/sola/my-take-on-sola.html` → `css/sola.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/sola/act-*.html` → `css/sola.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/sola/summary.html` → same as act pages
   - `pages/research/overview/harness/*.html` → `css/harness.css` (four levels up: `../../../../css/`); Acts 6–9 also load `css/concept-popup.css`
   - `pages/research/overview/cmb/cmb-topography-map.html` → `css/cmb-topography-map.css` (four levels up: `../../../../css/`)
   - `pages/research/publications/papers.html` → *(no dedicated stylesheet; uses `styles.css` only)*
   - `pages/research/posters/posters.html` → `css/posters.css`
   - `pages/research/posters/BSM24/BSM24.html` → `css/BSM24.css`

### CSS Path Convention

Pages in `pages/` link CSS with `../../css/styles.css` (two levels up).
Pages in `pages/research/overview/` link CSS with `../../../css/styles.css`.
Pages in `pages/research/overview/think-first/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/bayes/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/frequentist/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/sola/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/harness/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/cmb/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/publications/` link CSS with `../../../css/styles.css`.
Pages in `pages/research/posters/` link CSS with `../../../css/styles.css`.
Pages in `pages/research/posters/BSM24/` link CSS with `../../../../css/styles.css`.

`index.html` (root) links CSS with `css/styles.css`.

---

## Navigation

The site-wide `<nav>` is **manually replicated** in every HTML page's
`<header>` section. There is no server-side include or template system.

### Current Nav Structure

```html
<nav>
  <ul>
    <li><a href="...index.html">Home</a></li>
    <li><a href="...pages/about.html">About</a></li>
    <li class="dropdown">
      <a href="...pages/research/overview/index.html">Research</a>
      <div class="dropdown-content">
        <a href="...pages/research/publications/papers.html">Publications</a>
        <a href="...pages/research/posters/posters.html">Presentations</a>
      </div>
    </li>
    <li><a href="...pages/cv.html">CV</a></li>
    <li><a href="...pages/contacts.html">Contact</a></li>
  </ul>
</nav>
```

**CRITICAL**: When adding or removing a nav link, the change must be applied to
**every** HTML file in the repo. The relative `href` prefix varies by page depth:

| Page depth | Prefix to root |
|------------|----------------|
| `index.html` (root) | `` (no prefix) |
| `pages/*.html` | `../` |
| `pages/research/overview/*.html` | `../../../` |
| `pages/research/overview/think-first/*.html` | `../../../../` |
| `pages/research/overview/sola/*.html` | `../../../../` |
| `pages/research/overview/bayes/*.html` | `../../../../` |
| `pages/research/publications/*.html` | `../../../` |
| `pages/research/posters/posters.html` | `../../../` |
| `pages/research/posters/BSM24/BSM24.html` | `../../../../` |

---

## Page Inventory

| File | Title / Purpose |
|------|----------------|
| `index.html` | Home — hero section + recent highlights |
| `pages/about.html` | About — bio, background, interests |
| `pages/cv.html` | General professional and research CV aligned with the current public PDF: professional summary, impact-led capabilities and experience, open-source software, current education and thesis details, technical skills, publications, manuscripts in preparation, selected technical writing, linked presentations, and work/travel information |
| `media/Long_CV.pdf` | Three-page public CV generated from a separately maintained LaTeX source; unpublished works are titles only, with no private previews, credentials, telephone numbers, email addresses, or referee contact details |
| `pages/contacts.html` | Contact — email and social links |
| `pages/research/overview/index.html` | Research overview — summary of research topics + code links |
| `pages/research/overview/inversions-inferences.html` | Explainer: what are inversions and inferences |
| `pages/research/overview/bayes/bayes-measure-theoretically.html` | Bayes, Measure-Theoretically — landing page with overview and multi-page nav |
| `pages/research/overview/bayes/part-1.html` | Part 1: The Game — hidden switches, forward operator, unreliable reporter, prior |
| `pages/research/overview/bayes/part-2.html` | Part 2: The High-School Solution — joint table, predictive probabilities, posterior rule |
| `pages/research/overview/bayes/part-3.html` | Part 3: The Same Solution, Measure-Theoretically — measurable spaces, kernels, joint measure, posterior kernel |
| `pages/research/overview/bayes/part-4.html` | Part 4: Summary & Notation Map — two stories side by side, dictionary |
| `pages/research/overview/think-first/think-first-discretize-later.html` | Think First, Discretize Later — landing page with overview and multi-page nav |
| `pages/research/overview/think-first/act-1.html` | Act I: A Familiar Problem — naive discretization and the innocent-looking posterior |
| `pages/research/overview/think-first/act-2.html` | Act II: Something Is Wrong — sampling the posterior, invisible directions, divergent variance |
| `pages/research/overview/think-first/act-3.html` | Act III: What Problem Are We Actually Solving? — function-space Bayesian formulation |
| `pages/research/overview/think-first/act-4.html` | Act IV: A Guided Detour Through Functional Analysis — Hilbert spaces, Sobolev spaces, boundary conditions |
| `pages/research/overview/think-first/act-5.html` | Act V: The Data Space and the Adjoint — finite-dimensional data, Gram matrices, geometry-aware adjoint |
| `pages/research/overview/think-first/act-6.html` | Act VI: The Prior Is Not Just a Matrix — measure theory, Gaussian measures, trace-class covariance operators |
| `pages/research/overview/think-first/act-7.html` | Act VII: Putting the Pieces Together — function-space posterior, discretization after formulation |
| `pages/research/overview/think-first/act-8.html` | Act VIII: Return to the Toy Problem — corrected workflow, comparison with naive approach |
| `pages/research/overview/think-first/summary.html` | Summary of the Argument + Appendices A–D (Gaussian conditioning, Hilbert-space measures, Gram matrices, exercises) |
| `pages/research/overview/frequentist/bayesian-frequentist.html` | Bayesian and Frequentist Inference — landing page with overview and multi-page nav |
| `pages/research/overview/frequentist/part-1.html` | Part 1: The Setup — ontological observation equation, actual objects, identifiability |
| `pages/research/overview/frequentist/part-2.html` | Part 2: The Observation Kernel — noise model, candidate-dependent laws, what likelihood can/cannot say |
| `pages/research/overview/frequentist/part-3.html` | Part 3: The Bayesian Path — prior, joint measure, posterior, what collapses without a prior |
| `pages/research/overview/frequentist/part-4.html` | Part 4: The Frequentist Path — truth fixed, confidence sets, coverage, what frequentist does/doesn't claim |
| `pages/research/overview/frequentist/part-5.html` | Part 5: Beyond Additive Noise — general sampling laws, test statistics, decision rules |
| `pages/research/overview/sola/my-take-on-sola.html` | My Take on SOLA — landing page with overview and multi-page nav |
| `pages/research/overview/sola/act-1.html` | Act 1: The Kernel Game — sensitivity kernels, data as integrals, target kernels |
| `pages/research/overview/sola/act-2.html` | Act 2: Building SOLA from Scratch — weighted sums, resolving kernels, the minimization problem |
| `pages/research/overview/sola/act-3.html` | Act 3: Averages Need Mass — unimodularity constraint, constrained SOLA |
| `pages/research/overview/sola/act-4.html` | Act 4: Beyond Averages — derivative targets, basis coefficients, contrasts, resolving constraints |
| `pages/research/overview/sola/act-5.html` | Act 5: Noise Enters the Room — noisy data model, noise-aware SOLA, propagated covariance |
| `pages/research/overview/sola/act-6.html` | Act 6: What Did SOLA Actually Estimate? — approximate property map, honest sidestep |
| `pages/research/overview/sola/act-7.html` | Act 7: A Synthetic Cautionary Tale — apparent failure, manufacturing discrepancy, nullspace |
| `pages/research/overview/sola/act-8.html` | Act 8: SOLA as an Inversion in Disguise — proxy model, resolution operators |
| `pages/research/overview/sola/act-9.html` | Act 9: What About Uncertainty? — propagated noise vs posterior uncertainty, shifted-noise issue |
| `pages/research/overview/sola/act-10.html` | Act 10: Generative SOLA — pushing model-data relations through SOLA, where priors belong |
| `pages/research/overview/sola/act-11.html` | Act 11: What SOLA Is Good For — fair summary, ratios, final slogan |
| `pages/research/overview/sola/summary.html` | Summary of the Argument + Appendices A–C (algebra of minimizers, proxy model derivation, suggested figures) |
| `pages/research/overview/harness/the-machine-around-the-model.html` | The Machine Around the Model — landing page for the agentic-AI harness series |
| `pages/research/overview/harness/act-1.html` … `act-11.html` | Acts 1–11: model mechanics, chat harnesses, tool loops, coding-agent anatomy, AGENTS.md, skills, hooks, tools, context, and orchestration |
| `pages/research/overview/harness/agentic-structure-map.html` | Interactive relationship graph for this workspace's agentic components: context, abilities, the agent-documents SSD, evidence, and the live legacy continuity bridge |
| `pages/research/overview/harness/workspace-explorer.html` | Recursive VS Code-style explorer of selected real agent-related paths; it distinguishes the `docs/agent-docs` durable record store from separately selected abilities, and shows names and roles only, never file contents |
| `pages/research/overview/harness/summary.html` | Closing summary for The Machine Around the Model |
| `pages/research/overview/cmb/cmb-topography-map.html` | CMB Topography Studies — interactive timeline of CMB topography papers decoded through the ELEMENTS framework |
| `pages/research/publications/papers.html` | Publications list |
| `pages/research/posters/posters.html` | Presentations / posters gallery |
| `pages/research/posters/BSM24/BSM24.html` | BSM24 conference poster page |

---

## JavaScript

Vanilla JS (no framework) is used for page-specific interactivity. Scripts live in
`js/` and are linked at the bottom of the page before `</body>`.

| File | Used by | Purpose |
|------|---------|---------|
| `js/concept-popup.js` | Concept-enabled notes pages, including `overview/harness/act-6.html` through `act-9.html` | Accessible modal dialog for concept or source-document popups (click/Esc/overlay close, focus trap, MathJax re-typeset on open) |
| `js/refinement-panel.js` | `overview/think-first/think-first-discretize-later.html` | Interactive Plotly panel reading `refinement_sweep.json` (N-slider, naive/Bessel toggles, summary subplot) |
| `js/ai-assist.js` | All notes pages in `overview/sola/`, `overview/think-first/`, `overview/bayes/`, `overview/frequentist/` | "Read with AI" toolbar: Copy-for-AI button (fetches raw page HTML so LaTeX survives MathJax, prepends context preamble + macros), Open-in-ChatGPT prefill link, and AI companion link. Series auto-detected from URL path; per-series config (title, landing page, intent) lives in the `SERIES` map inside the script. Styles are injected by the script itself (no CSS file). |

External JS loaded via CDN:
- **MathJax 3** (`tex-chtml.js`) — used by `overview/bayes/bayes-measure-theoretically.html` (and all part pages), `overview/think-first/think-first-discretize-later.html` (and all act pages), and `overview/sola/my-take-on-sola.html` (and all act pages)
- **Plotly.js 2.35.2** — used by `overview/think-first/think-first-discretize-later.html`

---

## AI-Assisted Reading Infrastructure

Each notes series ships a plain-text **AI reading companion** at
`<series-dir>/ai-companion.txt` (narrative arc, notation, intent,
guardrails against common misreadings). These are linked from the
`ai-assist.js` toolbar and intended to be given to any LLM by readers.
`.txt` is used instead of `.md` because GitHub Pages runs Jekyll (no
`.nojekyll` file), which would transform `.md` files.

| Series | Companion |
|--------|-----------|
| My Take on SOLA | `pages/research/overview/sola/ai-companion.txt` |
| Think First, Discretize Later | `pages/research/overview/think-first/ai-companion.txt` |
| Bayes, Measure-Theoretically | `pages/research/overview/bayes/ai-companion.txt` |
| Bayesian and Frequentist Inference | `pages/research/overview/frequentist/ai-companion.txt` |

The site root contains **`llms.txt`** (llmstxt.org convention): an index of
the notes series, companions, and other pages with absolute URLs, for
discovery by AI tools.

**Checklist when adding/renaming a series or act:** update the `SERIES`
map in `js/ai-assist.js`, the series' `ai-companion.txt` (arc + titles),
and `llms.txt`.

---

## Cross-linking

The Think First, Discretize Later page is discoverable via:
1. **Research overview** (`overview/index.html`) → Featured Theory Topics card → `think-first/think-first-discretize-later.html`
2. **Presentations** (`posters/posters.html`) → EGU 2026 poster card → "Supplementary material" link → `overview/think-first/think-first-discretize-later.html`

The page links back to: EGU 2026 poster PDF, pygeoinf (GitHub), intervalinf (GitHub).

The landing page includes a multi-page navigation bar at the top
linking to `act-1.html` through `act-8.html` and `summary.html`. Each multi-page
act includes its own quick-nav bar and prev/next buttons.

It is **not** in the global nav dropdown (by design — see resolved decisions in the plan).

The Bayes, Measure-Theoretically page is discoverable via:
1. **Research overview** (`overview/index.html`) → Featured Theory Topics card → `bayes/bayes-measure-theoretically.html`

The landing page includes a multi-page navigation bar linking to `part-1.html`
through `part-4.html`. Each part page includes its own nav bar and prev/next buttons.

The Bayesian and Frequentist Inference page is discoverable via:
1. **Research overview** (`overview/index.html`) → Featured Theory Topics card → `frequentist/bayesian-frequentist.html`

The landing page includes a multi-page navigation bar linking to `part-1.html`
through `part-5.html`. Each part page includes its own nav bar and prev/next buttons.

The My Take on SOLA page is discoverable via:
1. **Research overview** (`overview/index.html`) → Featured Theory Topics card → `sola/my-take-on-sola.html`

The landing page includes a multi-page navigation bar linking to `act-1.html`
through `act-11.html` and `summary.html`. Each act page includes its own nav bar
(part-chip links) and prev/next buttons.

The Machine Around the Model is discoverable from the site navigation under **AI in
Practice**. Its landing page links to eleven acts and a summary. Act 6 reuses the shared
concept-popup component for one verbatim, scrollable snapshot of this website's own `AGENTS.md`
and contains an inline, static-data context inspector. Act 7 uses the same popup component for
real local skill files and contains an inline progressive-disclosure inspector. No file
contents are fetched at runtime. Act 8 exposes a website-local hook policy, wiring, and live
denial alongside a recorded interceptor. Act 9 exposes a website-local tool contract, handler
gate, and recorded calls, then reuses the screened Act 4 trace for its MCP example.

Two companion pages expose the workspace from different angles. `agentic-structure-map.html`
uses an original hardware-inspired board for readers who can code but are new to agents: context
injection, the next-token model, actions and selected skill kits, the `docs/agent-docs` SSD,
evidence checks, and the live legacy continuity bridge occupy distinct labelled regions. Skills
appear with abilities, not as SSD memory: the board links `website-control` to the private
bridge and `pdf-source-reading` to Citation Audit. Its interactive nodes open plain-language role
explanations; it does not fetch or reproduce private file contents. The context region separates
system prompt, ordinary tool descriptions, project/memory files, short skill metadata, retained
conversation, current prompt, and client-loaded-on-demand MCP tools; it marks the last as a
dated Claude-client observation rather than universal behaviour. The board visibly records the
date of its latest workspace review. Before a prompt, the
host supplies its session rules, tools, and short skill descriptions; a trusted Codex project
also supplies `.codex/config.toml` and `AGENTS.md`, while Claude reaches the shared bootstrap
through its unscoped rule. No workspace command runs merely from that context. In this workspace,
a prompt then starts the softly required `website-control` routine, which verifies the local
continuity packet before selecting any task records. A failed applicability check records only a
redacted local category and blocks ordinary workspace work until Git/source-based repair passes
the validator again. After that check, a general conversation may
need no further workspace material; other tasks may select the relevant plan, dossier, or living
reference before reaching the conditional site-change checklist, explicitly
run search/figure/mobile scripts, an optional browser ability, or the independent automatic Git
check. A blue outer return path makes the normal conversation loop visible: it is host/session
behaviour, not a local control-file rule, and returns one agent response to the next user prompt
without repeating bootstrap in the same continuous task. The
checklist distinguishes notes prose/search refresh, CSS or JavaScript/cache refresh,
navigation/manual copies, and browser validation; it does not imply that every branch runs for
every edit. The start-or-resume procedure does not repeat for every prompt. During a continuous
task, a new request or discovery triggers a smaller reassessment only when it materially changes
the objective, scope, evidence, or phase: the agent then continues small work, creates or uses a
plan, or updates the relevant active plan before returning to focused work. A meaningful close
refreshes the handoff for the next start-or-resume route. The map deliberately omits ordinary
source files and the Act 8–9 teaching exhibits.
`workspace-explorer.html` presents a
curated real file tree with recursive folder controls and a plain-language detail pane. The
explorer embeds names and role descriptions only; it never reads or serves workspace file
contents at runtime. Directory symlinks remain visibly labelled as shortcuts but can be
expanded like folders; the initially open `.agents/` route exposes the shared skill's bundled
`validate_control.py` without implying that a second copy exists. The desktop grid row and its
left and right panes are explicitly allowed to shrink; the tree and detail pane then own their
scrolling, so recursively expanded content is not clipped by the fixed-height shell. Each
explorer selection also explains whether it is automatically loaded, selected for a task, read
only when relevant, or explicitly run as a program. The relationship map adds selectable Codex,
Claude, and script routes: in a trusted project, Codex begins with both its project
`.codex/config.toml` layer and `AGENTS.md`, which point to the same bootstrap; Claude begins
from its unscoped `.claude/rules/` bootstrap adapter before both clients reach the shared skill.
The same routing guide also includes the independent Git commit route: this clone's configured
`.githooks/commit-msg` program runs automatically for local commits, including agent-made
commits, but is a warn-only Git check rather than an agent instruction or a universal server
policy. A separate Playwright MCP node is deliberately styled as an optional browser ability:
an enabled compatible client can make its tools visible to an agent, but no tracked workspace
workflow selects it or directs when to use it. Its ignored `.playwright-mcp/` folder is browser
scratch output, not automatic or durable agent memory. Selecting that folder in the explorer
adds a direct link back to the Playwright-MCP ability node and a route explanation that separates
the optional ability from the evidence it may leave behind.

Inside the website-control popup, the entrance sequence is directional: automatically supplied
workspace guidance leads a new or resumed task to `BOOTSTRAP.md`; that short note names
`website-control`; the agent then reads `SKILL.md`, which selects the remaining policy, state,
handoff, maintenance, and validator resources. The bootstrap is the first explicitly opened
local control file on that route, not a support file discovered after the skill starts and not a
file reread before every message in one continuous task. The popup continues with a scrollable,
numbered top-to-bottom spine that mirrors the skill's real start-or-resume order: resolve the
canonical skill/repository; read principles and handoff; compare identity with Git; run the
validator; conditionally fall back to source and Git if it fails; choose task scale; then read
current and only the tracked records needed for the task.

---

## Media Conventions

- Background images for hero sections live in `media/backgrounds/`.
- Use relative paths from the HTML file's location (e.g., `../../media/backgrounds/cygnus.jpg`).
- Poster PDFs and thumbnails live under `media/research/posters/`.
- Think First, Discretize Later figures (SVG/PNG) and `refinement_sweep.json` live under `media/research/think-first/`.
- Personal photos live under `media/personal/`.

---

## Adding a New Page — Checklist

1. Create `pages/research/<page-name>.html` (or appropriate subdirectory).
2. Create `css/<page-name>.css` for page-specific styles.
3. Link both `styles.css` and the new CSS file in the `<head>` with correct relative paths.
4. Copy the `<nav>` block from an existing page at the same depth, adjusting `href` prefixes.
5. Add a link to the new page in the `<nav>` dropdown (or top-level) of **every** existing HTML file.
6. Update this living reference: page inventory, CSS pairing table, and nav structure.
