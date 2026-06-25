"""Figure F8b - Naive vs corrected posterior samples, side-by-side.

Same N, same data, same true model. Left: naive posterior samples.
Right: corrected (Bessel) posterior samples. Identical axes, same number
of samples, same styling. Let the mathematics do the talking.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

N_CELLS = 30
N_SAMPLES = 8
N_STD_SAMPLES = 200


def _posterior(forward, data, box, prior, data_space, x):
    g_disc = LinearOperator.from_formal_adjoint(
        box.coeff_space, data_space,
        forward @ box.function_space.coordinate_inclusion,
    )
    problem = LinearForwardProblem(
        g_disc, data_error_measure=ps.data_error_measure(data, data_space),
    )
    inv = LinearBayesianInversion(problem, prior, formalism="data_space")
    return inv.model_posterior_measure(data.d, CholeskySolver())


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    x = ps.plot_grid()
    bessel_cov = ps.make_bessel_covariance(model_space)
    data_space = forward.codomain

    box = ps.hat_coeff_space(N_CELLS)
    fs = box.function_space

    # Naive posterior
    naive_prior = ps.discrete_prior("naive", box)
    naive_post = _posterior(forward, data, box, naive_prior, data_space, x)
    naive_mean = np.asarray(fs.from_components(naive_post.expectation).evaluate(x), float)
    naive_samples = np.asarray(
        [np.asarray(fs.from_components(naive_post.sample()).evaluate(x), float)
         for _ in range(N_SAMPLES)],
        dtype=float,
    )
    naive_std_samples = np.asarray(
        [np.asarray(fs.from_components(naive_post.sample()).evaluate(x), float)
         for _ in range(N_STD_SAMPLES)],
        dtype=float,
    )
    naive_std = naive_std_samples.std(axis=0)

    # Bessel posterior
    bessel_prior = ps.discrete_prior("bessel", box, bessel_covariance=bessel_cov)
    bessel_post = _posterior(forward, data, box, bessel_prior, data_space, x)
    bessel_mean = np.asarray(fs.from_components(bessel_post.expectation).evaluate(x), float)
    bessel_samples = np.asarray(
        [np.asarray(fs.from_components(bessel_post.sample()).evaluate(x), float)
         for _ in range(N_SAMPLES)],
        dtype=float,
    )
    bessel_std_samples = np.asarray(
        [np.asarray(fs.from_components(bessel_post.sample()).evaluate(x), float)
         for _ in range(N_STD_SAMPLES)],
        dtype=float,
    )
    bessel_std = bessel_std_samples.std(axis=0)

    true_vals = np.asarray(m_bar.evaluate(x), float)

    # Independent y-limits per panel (naive std ~8, corrected std ~0.05)
    naive_all = np.concatenate([naive_samples.ravel(), naive_mean])
    bessel_all = np.concatenate([bessel_samples.ravel(), bessel_mean])
    y_lo_n = float(min(naive_all.min(), true_vals.min())) - 0.5
    y_hi_n = float(max(naive_all.max(), true_vals.max())) + 0.5
    y_lo_c = float(min(bessel_all.min(), true_vals.min())) - 0.3
    y_hi_c = float(max(bessel_all.max(), true_vals.max())) + 0.3

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    colors = mako_light_n(N_SAMPLES)

    # Left: naive
    ax = axes[0]
    ax.fill_between(x, naive_mean - naive_std, naive_mean + naive_std,
                    color=PALETTE["naive"], alpha=0.10)
    for s in range(N_SAMPLES):
        ax.plot(x, naive_samples[s], color=colors[s], alpha=0.3, lw=1.0)
    ax.plot(x, naive_mean, color=PALETTE["naive"], lw=2.2,
            label="posterior mean")
    ax.plot(x, true_vals, color=PALETTE["true"], lw=2.4,
            label=r"true model $\bar{m}(z)$")
    ax.set_title(rf"Naive  $\mathbf{{C}}_N = \sigma^2 \mathbf{{I}}_N$  ($N={N_CELLS}$)")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.set_ylim(y_lo_n, y_hi_n)
    ax.legend(fontsize=10, loc="upper right")

    # Right: corrected
    ax = axes[1]
    ax.fill_between(x, bessel_mean - bessel_std, bessel_mean + bessel_std,
                    color=PALETTE["correct"], alpha=0.12)
    for s in range(N_SAMPLES):
        ax.plot(x, bessel_samples[s], color=colors[s], alpha=0.35, lw=1.0)
    ax.plot(x, bessel_mean, color=PALETTE["correct"], lw=2.2,
            label="posterior mean")
    ax.plot(x, true_vals, color=PALETTE["true"], lw=2.4,
            label=r"true model $\bar{m}(z)$")
    ax.set_title(
        rf"Corrected  $C_{{0,N}} \approx \alpha(\kappa^2 I - \Delta)^{{-s}}$  ($N={N_CELLS}$)"
    )
    ax.set_xlabel(r"depth $z$")
    ax.set_ylim(y_lo_c, y_hi_c)
    ax.legend(fontsize=10, loc="upper right")

    fig.tight_layout()
    save(fig, "fig8b_naive_vs_corrected_samples", ps.output_dir())
    print("wrote fig8b_naive_vs_corrected_samples")


if __name__ == "__main__":
    main()
