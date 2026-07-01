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
        publications/
            papers.html
        posters/
            posters.html
            BSM24/
                BSM24.html
media/
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
        references/
            living/
                website-reference.md   # ← this file
plans/
    active-plans/                   # Agent plans in progress
    completed-plans/                # Archived finished plans
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
   - `pages/research/overview/bayes/bayes-measure-theoretically.html` → `css/bayes-measure-theoretically.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/bayes/part-*.html` → `css/bayes-measure-theoretically.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/think-first/think-first-discretize-later.html` → `css/think-first-discretize-later.css` + `css/concept-popup.css` + `css/refinement-panel.css`
   - `pages/research/overview/think-first/act-*.html` → `css/think-first-discretize-later.css` + `css/concept-popup.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/think-first/summary.html` → same as act pages
   - `pages/research/overview/sola/my-take-on-sola.html` → `css/sola.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/sola/act-*.html` → `css/sola.css` (four levels up: `../../../../css/`)
   - `pages/research/overview/sola/summary.html` → same as act pages
   - `pages/research/publications/papers.html` → *(no dedicated stylesheet; uses `styles.css` only)*
   - `pages/research/posters/posters.html` → `css/posters.css`
   - `pages/research/posters/BSM24/BSM24.html` → `css/BSM24.css`

### CSS Path Convention

Pages in `pages/` link CSS with `../../css/styles.css` (two levels up).
Pages in `pages/research/overview/` link CSS with `../../../css/styles.css`.
Pages in `pages/research/overview/think-first/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/bayes/` link CSS with `../../../../css/styles.css`.
Pages in `pages/research/overview/sola/` link CSS with `../../../../css/styles.css`.
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
| `pages/cv.html` | CV — academic curriculum vitae |
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
| `pages/research/publications/papers.html` | Publications list |
| `pages/research/posters/posters.html` | Presentations / posters gallery |
| `pages/research/posters/BSM24/BSM24.html` | BSM24 conference poster page |

---

## JavaScript

Vanilla JS (no framework) is used for page-specific interactivity. Scripts live in
`js/` and are linked at the bottom of the page before `</body>`.

| File | Used by | Purpose |
|------|---------|---------|
| `js/concept-popup.js` | `overview/think-first/think-first-discretize-later.html` | Accessible modal dialog for concept-term popups (click/Esc/overlay close, focus trap, MathJax re-typeset on open) |
| `js/refinement-panel.js` | `overview/think-first/think-first-discretize-later.html` | Interactive Plotly panel reading `refinement_sweep.json` (N-slider, naive/Bessel toggles, summary subplot) |

External JS loaded via CDN:
- **MathJax 3** (`tex-chtml.js`) — used by `overview/bayes/bayes-measure-theoretically.html` (and all part pages), `overview/think-first/think-first-discretize-later.html` (and all act pages), and `overview/sola/my-take-on-sola.html` (and all act pages)
- **Plotly.js 2.35.2** — used by `overview/think-first/think-first-discretize-later.html`

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

The My Take on SOLA page is discoverable via:
1. **Research overview** (`overview/index.html`) → Featured Theory Topics card → `sola/my-take-on-sola.html`

The landing page includes a multi-page navigation bar linking to `act-1.html`
through `act-11.html` and `summary.html`. Each act page includes its own nav bar
(part-chip links) and prev/next buttons.

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
