# Figure generation (offline tooling)

Python tooling that generates the figures and data bundles embedded in the
website's research explainer pages. **This is not part of the served static
site** — it runs offline, on demand, and writes image/JSON assets into
`media/`. The website itself remains plain HTML/CSS with no build step.

## Environment

The scripts import [`intervalinf`](../../Inferences) and `pygeoinf`, which live
in the `inferences` conda environment (not in this repo). Run everything through
that environment:

```bash
conda run -n inferences python figure_generation/think_first_discretize_later/fig1_setup.py
```

There is no `requirements.txt` here on purpose: the dependencies are the research
libraries managed in their own repositories. If `intervalinf`/`pygeoinf` are not
installed in the `inferences` env, these scripts will not run.

## `think_first_discretize_later/`

Tooling for the **"Think First, Discretize Later"** page. One small 1-D linear
inverse problem on `[0, 1]` (a SOLA operator with Gaussian sensitivity kernels)
is shared by every figure, defined in `problem_setup.py`. Styling that blends
with the site's dark theme lives in `style.py`.

| Script | Output | What it shows |
| --- | --- | --- |
| `fig1_setup.py` | `fig1_setup.{png,svg}` | The model is a function; data are a few noisy integrals. |
| `fig2_naive_boxcar.py` | `fig2_naive_boxcar.{png,svg}` | Naive (transpose-as-adjoint) recovery on boxcars **looks fine** — the trap. |
| `fig3_geometry_hat.py` | `fig3_geometry_hat.{png,svg}` | On hat functions naive != correct; the Gram matrix explains why. |
| `fig4_refinement.py` | `fig4_refinement.{png,svg}` | Posterior under refinement: naive `sigma^2 I` diverges, Bessel converges. |
| `fig5_boundary_conditions.py` | `fig5_boundary_conditions.{png,svg}` | Boundary conditions as prior beliefs (Neumann vs Dirichlet-Neumann). |
| `make_interactive_data.py` | `refinement_sweep.json` | Per-N posterior curves for the page's interactive N-slider. |

All outputs are written to `media/research/think-first/`.

### Run everything

```bash
# fast figures (seconds each)
for f in fig1_setup fig2_naive_boxcar fig3_geometry_hat fig5_boundary_conditions; do
  conda run -n inferences python figure_generation/think_first_discretize_later/$f.py
done

# slow figures (a few minutes - real Bayesian posteriors at several resolutions)
conda run -n inferences python figure_generation/think_first_discretize_later/fig4_refinement.py
conda run -n inferences python figure_generation/think_first_discretize_later/make_interactive_data.py
```

### The core idea (in two numbers)

A discretised forward operator `G` has a coefficient-space adjoint that depends
on the basis Gram (mass) matrix `M`: the geometry-correct adjoint is `M^-1 G^T`,
**not** the bare transpose `G^T`. The naive transpose is only accidentally right
when `M` is diagonal:

- **Boxcars** (orthogonal): `M = h I`, so naive == correct — `max|naive-correct| ~ 1e-3`.
- **Hats** (overlapping): `M` is tridiagonal, so naive != correct — `max|naive-correct| ~ 0.18`.

### Tests

```bash
conda run -n inferences python -m pytest figure_generation/think_first_discretize_later/tests
conda run -n inferences python -m pytest figure_generation/think_first_discretize_later/tests -m "not slow"
```

### Provenance

The posterior-under-refinement method (`fig4`) mirrors the original EGU poster
script `fig10_posterior_grid.py` (boxcar discretisation, mass-weighted coefficient
space, `LinearBayesianInversion` with a naive `sigma*I` prior vs a trace-class
`BesselSobolevInverse` covariance), adapted to the shared `[0, 1]` problem.
