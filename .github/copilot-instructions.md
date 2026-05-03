# Inferences Workspace — Copilot Instructions

## What This Repository Is

A scientific Python monorepo for geophysical inverse-problem research. It contains four editable packages and a collection of notebooks / demos.

| Package | Purpose | Primary module |
|---------|---------|----------------|
| **pygeoinf** | Core inversion library: Hilbert spaces, linear/nonlinear operators, convex analysis, optimisation, Backus–Gilbert | `pygeoinf/` |
| **intervalinf** | Interval-domain functional analysis: Lebesgue spaces, SOLA operators, kernel providers, sampling | `intervalinf/` |
| **pygeoinf3D** | 3-D extensions of pygeoinf | `pygeoinf3d/` |
| **simple_regional_tomography_example** | Seismic tomography teaching demo | `seismic_tomo/` |

## Environment Setup

- **Conda environment:** `inferences3` (Python 3.11) — always activate before running code or tests.
- Install editable packages: `cd <package> && pip install -e .[dev]`
- The workspace root `.venv/` is legacy Python 3.8 — **do not use**.

## Running Tests

```bash
conda activate inferences3
cd pygeoinf && python -m pytest tests/ -x -q
cd ../intervalinf && python -m pytest tests/ -x -q
```

Always run the individual test file first, then the full suite to catch regressions.

## Code Conventions

- **Docstrings:** Google-style with LaTeX math (`$...$` or `$$...$$`). Include algorithm references as `Author (Year)` or DOI.
- **Type hints:** Use `np.ndarray`; document array shapes in docstrings.
- **Numerical tests:** Use `np.testing.assert_allclose` with explicit `rtol`/`atol`. Set random seeds for reproducibility.
- **Vectorisation:** Prefer numpy/scipy operations over Python loops.

## Commit Convention

All feature/fix commits must include plan references. See `COMMIT_CONVENTION.md` for the full format. Key fields:

```
<type>(<scope>): <subject>

- specific change

Plan: <relative-path-to-plan>
Phase: <N> of <total>
Related: <relative-path-to-phase-complete>
```

## Plan Directories

Each package has its own plan directory under `docs/agent-docs/`:
- `pygeoinf/docs/agent-docs/` — active-plans, completed-plans, references, theory on agent/private branches; shared collaboration branches may intentionally omit committed agent-doc files
- `intervalinf/docs/agent-docs/` — same layout
- `pygeoinf3D/docs/agent-docs/` — same layout
- `simple_regional_tomography_example/plans/` — plan/archive location for committed agent artifacts in the teaching demo
- Check the package-specific `AGENTS.md` for any overrides.

## Living Reference Documents

Before exploring a package's source files, check for condensed reference docs at:
```
<package>/docs/agent-docs/references/living/*-reference.md
```
Read **all** living references before individual file reads. Never consult `references/legacy/`.
If a package has no committed living references, proceed with normal source exploration. On shared `pygeoinf` branches this can be intentional.
After modifying a package, update its living references to reflect changes.

## Remote Execution (europa)

Heavy computations run on a remote university PC via the `europa` skill. Key rules:
1. Always check VPN: `europa status`
2. Check disk: `europa df` (need >500 MB free)
3. Claim slot before running: `europa claim INFERENCES <mission_id>`
4. Release when done: `europa release INFERENCES complete`

Mission IDs must include workspace name: `MISSION_YYYYMMDD_INFERENCES_<task>`.

## Key Dependencies

numpy, scipy, matplotlib (core); pyshtools (spherical harmonics); Cartopy (geographic plots). See `pygeoinf/pyproject.toml` for extras.
