---
name: repo-orientation
description: "Orient an agent in the Inferences monorepo. Use when: starting work on any package, exploring unfamiliar code, or onboarding to a new task. Identifies the package layout, living references, plan directories, and conda environment."
---

# Repo Orientation

Follow these steps to orient yourself before doing any work in this monorepo.

## 1. Identify the target package

| Package | Source dir | Test dir |
|---------|-----------|----------|
| pygeoinf | `pygeoinf/pygeoinf/` | `pygeoinf/tests/` |
| intervalinf | `intervalinf/intervalinf/` | `intervalinf/tests/` |
| pygeoinf3D | `pygeoinf3D/pygeoinf3d/` | `pygeoinf3D/tests/` |
| simple_regional_tomography_example | `simple_regional_tomography_example/seismic_tomo/` | `simple_regional_tomography_example/tests/` |

## 2. Read living references (MANDATORY before file exploration)

```
<package>/docs/agent-docs/references/living/*-reference.md
```

Read **every** file in the `living/` directory. These contain architecture, class hierarchy, public API, and file mappings. Only read individual source files for details not covered.

If the `living/` directory is absent, continue with normal source exploration. On shared `pygeoinf` branches, missing committed agent-doc files can be intentional.

**Never** read from `references/legacy/` — those are archived and may be stale.

## 3. Check package-level AGENTS.md

Some packages have a local `AGENTS.md` with plan directory overrides or package-specific conventions. Check for it at `<package>/AGENTS.md`.

## 4. Locate the plan directory

Default layout:
- `<package>/docs/agent-docs/active-plans/` — current plans
- `<package>/docs/agent-docs/completed-plans/` — finished plans

Exceptions:
- `simple_regional_tomography_example/plans/` stores committed plan artifacts for the teaching demo.
- Shared `pygeoinf` branches may intentionally omit committed `docs/agent-docs/` content.

## 5. Confirm environment

```bash
conda activate inferences3
```

Python 3.11. Do **not** use the workspace root `.venv/` (legacy Python 3.8).

## 6. After making changes

Update all affected living reference files to reflect additions, removals, or signature changes. Stale references mislead future agents.
