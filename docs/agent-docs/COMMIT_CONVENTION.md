# Commit Message Convention

## Purpose

This convention ensures **traceability** between site changes and planning documents. When a layout regression or broken link appears later, the commit history traces back to the plan that introduced it.

## Format

```
<type>(<scope>): <subject>

<body: bullet points of specific changes>

Plan: <path-to-plan>
Phase: <current> of <total>
Related: <path-to-phase-complete-document>
```

### Components

**Type**: One of `feat`, `fix`, `refactor`, `style`, `content`, `docs`, `chore`
- Use `feat` for new pages, new sections, or new site features
- Use `fix` for broken links, layout bugs, or incorrect content
- Use `refactor` for restructuring HTML/CSS without changing appearance
- Use `style` for visual/design changes (colors, spacing, typography)
- Use `content` for text-only updates (no structural or visual change)
- Use `docs` for updating README or agent documentation (no Plan line needed)
- Use `chore` for tooling or configuration changes (no Plan line needed)

**Scope**: The primary page or component affected (e.g., `index`, `about`, `research`, `cv`, `nav`, `css`)

**Subject**: 50 characters or less, imperative mood

**Body**:
- Format as bullet points (lines starting with `-`)
- Describe specific changes (pages modified, CSS rules added, links fixed)
- Keep each bullet concise (40–60 characters)

**Plan**: Workspace-relative path to the plan document
- Example: `plans/active-plans/research-page-redesign-plan.md`
- Use relative paths from workspace root

**Phase**: Current phase being completed (use `N/A` if not applicable)
- Format: `<current-number> of <total-number>`
- Examples: `1 of 1`, `2 of 4`, `N/A`

**Related**: Workspace-relative path to the phase-complete markdown
- Example: `plans/completed-plans/research-page-redesign-phase-1-complete.md`
- Include this **only if a phase-complete document exists**

## Examples

### New Page (Single Phase)
```
feat(research): add SOLA-DLI research page

- Create pages/research/sola-dli.html with full content
- Add sola-dli.css for page-specific styling
- Link new page in site-wide navigation

Plan: plans/completed-plans/sola-dli-page-plan.md
Phase: 1 of 1
Related: plans/completed-plans/sola-dli-page-phase-1-complete.md
```

### Multi-Phase Redesign
```
style(index): redesign hero section layout

- Replace full-bleed background with contained card
- Update typography scale for headings
- Add responsive breakpoints for mobile

Plan: plans/active-plans/homepage-redesign-plan.md
Phase: 2 of 3
Related: plans/completed-plans/homepage-redesign-phase-2-complete.md
```

### Content Update (No Plan Needed)
```
content(cv): update publications list for 2026

- Add three new journal articles
- Fix author ordering in 2025 entry
```

### Bug Fix
```
fix(nav): correct broken link to posters page

- Update href from /posters to pages/research/posters/posters.html

Plan: N/A
Phase: N/A
```
