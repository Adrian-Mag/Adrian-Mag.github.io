---
name: tdd-scientific-python
description: "Test-driven development workflow for scientific Python code. Use when: implementing operators, support functions, optimizers, or any mathematical code in pygeoinf or intervalinf. Covers red-green-refactor with numpy testing patterns, LaTeX docstrings, and numerical edge cases."
---

# TDD for Scientific Python

Follow this workflow when implementing any mathematical or scientific code.

## Red Phase — Write Failing Tests First

1. Create test file at `<package>/tests/<subdir>/test_<feature>.py`
2. Use `np.testing.assert_allclose` with explicit `rtol`/`atol`
3. Set random seeds: `np.random.seed(42)` or `rng = np.random.default_rng(42)`
4. Include tests for:
   - **Basic correctness**: known input → expected output
   - **Mathematical properties**: convexity, adjoint identity, positive homogeneity
   - **Edge cases**: `q=0`, singular matrices, empty arrays, NaN/Inf
   - **Symmetry/invariance**: if theory predicts it, test it
5. Run: `python -m pytest tests/<subdir>/test_<feature>.py -x -q` — must FAIL

## Green Phase — Minimal Implementation

1. Write only enough code to make the tests pass
2. Use numpy/scipy vectorized operations (no Python loops for array work)
3. Add LaTeX docstrings with theory references:
   ```python
   def support_function(self, q):
       """Evaluate $\\sigma_C(q) = \\sup_{x \\in C} \\langle q, x \\rangle$.

       See theory.txt §2.2, Equation (2.1).

       Args:
           q: Direction vector, array of shape ``(n,)``.

       Returns:
           float: Support value $\\sigma_C(q)$.
       """
   ```
4. Run: `python -m pytest tests/<subdir>/test_<feature>.py -x -q` — must PASS

## Refactor Phase

1. Clean up implementation without changing behavior
2. Run full test suite: `python -m pytest tests/ -x -q` — must PASS (no regressions)

## Post-Implementation

1. Update living reference documents
2. Report file list, function list, and test results to the orchestrating agent
