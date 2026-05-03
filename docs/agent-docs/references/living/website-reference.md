# Website Living Reference

## Scope

This document describes the structure, conventions, and file mappings for the
`Adrian-Mag.github.io` static website. Read this before modifying any page or
stylesheet. Update this file whenever pages, CSS files, or navigation links are
added, removed, or restructured.

---

## Site Architecture

The site is **plain HTML5 + CSS3** with no build step, no JavaScript framework,
and no preprocessor. All pages are served directly by GitHub Pages.

### Directory Layout

```
index.html                          # Home page (root)
output.html                         # (legacy/scratch output page)
css/                                # All stylesheets
pages/
    about.html
    contacts.html
    cv.html
    research/
        research_overview.html
        papers.html
        inversions-inferences.html
        math-details.html
        pli-methods.html
        sola-dli.html
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
docs/
    agent-docs/
        references/
            living/
                website-reference.md   # ← this file
plans/
    active-plans/                   # Agent plans in progress
    completed-plans/                # Archived finished plans
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
   - `pages/research/research_overview.html` → `css/research_overview.css`
   - `pages/research/papers.html` → *(no dedicated stylesheet; uses `styles.css` only)*
   - `pages/research/inversions-inferences.html` → *(no dedicated stylesheet)*
   - `pages/research/math-details.html` → `css/math-details.css`
   - `pages/research/pli-methods.html` → `css/pli-methods.css`
   - `pages/research/sola-dli.html` → `css/sola-dli.css`
   - `pages/research/posters/posters.html` → `css/posters.css`
   - `pages/research/posters/BSM24/BSM24.html` → `css/BSM24.css`

### CSS Path Convention

Pages in `pages/` link CSS with `../../css/styles.css` (two levels up).
Pages in `pages/research/` link CSS with `../../css/styles.css`.
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
      <a href="...pages/research/research_overview.html">Research</a>
      <div class="dropdown-content">
        <a href="...pages/research/papers.html">Publications</a>
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
| `pages/research/*.html` | `../../` |
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
| `pages/research/research_overview.html` | Research overview — summary of research topics |
| `pages/research/papers.html` | Publications list |
| `pages/research/inversions-inferences.html` | Explainer: what are inversions and inferences |
| `pages/research/math-details.html` | Mathematical details of methods |
| `pages/research/pli-methods.html` | PLI methods research page |
| `pages/research/sola-dli.html` | SOLA-DLI research page |
| `pages/research/posters/posters.html` | Presentations / posters gallery |
| `pages/research/posters/BSM24/BSM24.html` | BSM24 conference poster page |

---

## Media Conventions

- Background images for hero sections live in `media/backgrounds/`.
- Use relative paths from the HTML file's location (e.g., `../../media/backgrounds/cygnus.jpg`).
- Poster PDFs and thumbnails live under `media/research/posters/`.
- Personal photos live under `media/personal/`.

---

## Adding a New Page — Checklist

1. Create `pages/research/<page-name>.html` (or appropriate subdirectory).
2. Create `css/<page-name>.css` for page-specific styles.
3. Link both `styles.css` and the new CSS file in the `<head>` with correct relative paths.
4. Copy the `<nav>` block from an existing page at the same depth, adjusting `href` prefixes.
5. Add a link to the new page in the `<nav>` dropdown (or top-level) of **every** existing HTML file.
6. Update this living reference: page inventory, CSS pairing table, and nav structure.
