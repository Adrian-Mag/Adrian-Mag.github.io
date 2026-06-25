"""Figure F8c (static) - Naive vs corrected refinement grid.

Renders a static PNG comparison of the two workflows under mesh refinement.
Top row: naive posterior at N = 21, 35, 50 (shared symmetric y-axis).
Bottom row: corrected (Bessel) posterior at the same N (shared y-axis).

Self-contained: computes the three resolutions' posteriors directly from
``problem_setup`` (the interactive 30-resolution slider it once replaced has
been retired, so no precomputed data file is needed).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

N_SHOW = [21, 35, 50]
N_GRID = 200
N_STD_SAMPLES = 100


def _posterior_curves(kind, n, *, forward, data, data_space, x,
                       bessel_cov=None):
    """Return (mean, std) on the plotting grid for the given prior kind and N."""
    box = ps.hat_coeff_space(n)
    fs = box.function_space
    data_err = ps.data_error_measure(data, data_space)
    g_disc = LinearOperator.from_formal_adjoint(
        box.coeff_space, data_space, forward @ fs.coordinate_inclusion,
    )
    prior = ps.discrete_prior(kind, box, bessel_covariance=bessel_cov)
    problem = LinearForwardProblem(g_disc, data_error_measure=data_err)
    inv = LinearBayesianInversion(problem, prior, formalism="data_space")
    post = inv.model_posterior_measure(data.d, CholeskySolver())
    mean = np.asarray(fs.from_components(post.expectation).evaluate(x), float)
    samples = np.asarray(
        [np.asarray(fs.from_components(post.sample()).evaluate(x), float)
         for _ in range(N_STD_SAMPLES)],
        dtype=float,
    )
    return mean, samples.std(axis=0)


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    data_space = forward.codomain
    bessel_cov = ps.make_bessel_covariance(model_space)
    x = np.linspace(ps.DOMAIN[0], ps.DOMAIN[1], N_GRID)
    m_true = np.asarray(m_bar.evaluate(x), float)

    naive = {}
    bessel = {}
    for n in N_SHOW:
        nm, nstd = _posterior_curves("naive", n, forward=forward, data=data,
                                     data_space=data_space, x=x)
        bm, bstd = _posterior_curves("bessel", n, forward=forward, data=data,
                                     data_space=data_space, x=x,
                                     bessel_cov=bessel_cov)
        naive[str(n)] = {"mean": nm, "std": nstd}
        bessel[str(n)] = {"mean": bm, "std": bstd}
        print(f"  N={n}: naive max-std={nstd.max():.2f}  "
              f"bessel max-std={bstd.max():.3f}", flush=True)

    # Shared y-limits per row.
    naive_max = 0.0
    for n in N_SHOW:
        mean, std = naive[str(n)]["mean"], naive[str(n)]["std"]
        naive_max = max(naive_max, float(np.max(np.abs(mean) + std)))
    y_lo_n, y_hi_n = -naive_max * 1.05, naive_max * 1.05

    bessel_lo = 0.0
    bessel_hi = 0.0
    for n in N_SHOW:
        mean, std = bessel[str(n)]["mean"], bessel[str(n)]["std"]
        bessel_lo = min(bessel_lo, float(np.min(mean - std)))
        bessel_hi = max(bessel_hi, float(np.max(mean + std)))
    pad = 0.1 * (bessel_hi - bessel_lo)
    y_lo_c, y_hi_c = bessel_lo - pad, bessel_hi + pad

    fig, axes = plt.subplots(2, len(N_SHOW), figsize=(15, 8), sharex=True)

    for col, n in enumerate(N_SHOW):
        # Top: naive
        ax = axes[0, col]
        mean = naive[str(n)]["mean"]
        std = naive[str(n)]["std"]
        ax.fill_between(x, mean - std, mean + std,
                        color=PALETTE["naive"], alpha=0.18, lw=0)
        ax.plot(x, mean, color=PALETTE["naive"], lw=2.2, label="posterior mean")
        ax.plot(x, m_true, color=PALETTE["true"], lw=2.0,
                label=r"true model $\bar{m}(z)$")
        ax.set_ylim(y_lo_n, y_hi_n)
        ax.set_title(rf"Naive  ($N={n}$),  max $\sigma={std.max():.1f}$")
        if col == 0:
            ax.set_ylabel("model value")
        if col == len(N_SHOW) - 1:
            ax.legend(fontsize=10, loc="upper right")

        # Bottom: corrected
        ax = axes[1, col]
        mean = bessel[str(n)]["mean"]
        std = bessel[str(n)]["std"]
        ax.fill_between(x, mean - std, mean + std,
                        color=PALETTE["correct"], alpha=0.20, lw=0)
        ax.plot(x, mean, color=PALETTE["correct"], lw=2.2, label="posterior mean")
        ax.plot(x, m_true, color=PALETTE["true"], lw=2.0,
                label=r"true model $\bar{m}(z)$")
        ax.set_ylim(y_lo_c, y_hi_c)
        ax.set_title(rf"Corrected  ($N={n}$),  max $\sigma={std.max():.3f}$")
        ax.set_xlabel(r"depth $z$")
        if col == 0:
            ax.set_ylabel("model value")
        if col == len(N_SHOW) - 1:
            ax.legend(fontsize=10, loc="upper right")

    fig.suptitle(
        "Posterior under mesh refinement: naive inflates, corrected settles",
        fontsize=17, y=0.99,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save(fig, "fig8c_refinement_grid", ps.output_dir())
    print("wrote fig8c_refinement_grid")


if __name__ == "__main__":
    main()
