"""Figure F7a - Corrected prior samples vs naive prior samples, same N.

Left: naive prior samples (sigma^2 I) on hat basis — ghosted/reference.
Right: Bessel/operator prior samples on same hat basis — the real prior.
Bottom: eigenvalue decay or cumulative trace for both priors.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save

N_CELLS = 30
N_SAMPLES = 8


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    x = ps.plot_grid()
    bessel_cov = ps.make_bessel_covariance(model_space)

    box = ps.hat_coeff_space(N_CELLS)
    fs = box.function_space

    # --- Naive prior samples ---
    rng_naive = np.random.default_rng(42)
    naive_coeffs = rng_naive.normal(0.0, ps.NAIVE_SIGMA, size=(N_SAMPLES, N_CELLS))
    naive_curves = np.asarray(
        [np.asarray(fs.from_components(c).evaluate(x), float) for c in naive_coeffs],
        dtype=float,
    )

    # --- Bessel prior samples ---
    bessel_prior = ps.discrete_prior("bessel", box, bessel_covariance=bessel_cov)
    bessel_cov_mat = bessel_prior.covariance.matrix(dense=True)
    # Symmetrise and PSD-clip
    bessel_cov_mat = 0.5 * (bessel_cov_mat + bessel_cov_mat.T)
    evals, evecs = np.linalg.eigh(bessel_cov_mat)
    evals = np.clip(evals, 0, None)
    sqrt_cov = evecs * np.sqrt(evals)
    rng_bessel = np.random.default_rng(42)
    bessel_coeffs = np.asarray(
        [bessel_prior.expectation + sqrt_cov @ rng_bessel.standard_normal(N_CELLS)
         for _ in range(N_SAMPLES)],
        dtype=float,
    )
    bessel_curves = np.asarray(
        [np.asarray(fs.from_components(c).evaluate(x), float) for c in bessel_coeffs],
        dtype=float,
    )

    # --- Eigenvalues for bottom panel ---
    naive_evals = np.full(N_CELLS, ps.NAIVE_SIGMA ** 2)
    bessel_evals = np.sort(evals)[::-1]

    # --- Plot ---
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.55], hspace=0.35, wspace=0.18)

    # (a) Naive prior samples — ghosted
    ax_naive = fig.add_subplot(gs[0, 0])
    colors = mako_light_n(N_SAMPLES)
    for s in range(N_SAMPLES):
        ax_naive.plot(x, naive_curves[s], color=colors[s], alpha=0.35, lw=1.0)
    ax_naive.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.4,
                  label=r"true model $\bar{m}(z)$")
    ax_naive.axhline(0, color=PALETTE["muted"], lw=1.2, linestyle="--", alpha=0.5)
    ax_naive.set_title(rf"(a) Naive prior  $\mathbf{{C}}_N = \sigma^2 \mathbf{{I}}_N$  ($N={N_CELLS}$)")
    ax_naive.set_xlabel(r"depth $z$")
    ax_naive.set_ylabel("model value")
    ax_naive.legend(fontsize=10, loc="upper right")

    # (b) Bessel prior samples — bright
    ax_bessel = fig.add_subplot(gs[0, 1])
    for s in range(N_SAMPLES):
        ax_bessel.plot(x, bessel_curves[s], color=colors[s], alpha=0.5, lw=1.2)
    ax_bessel.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.4,
                   label=r"true model $\bar{m}(z)$")
    ax_bessel.axhline(0, color=PALETTE["muted"], lw=1.2, linestyle="--", alpha=0.5)
    ax_bessel.set_title(
        rf"(b) Operator prior  $C_{{0,N}} \approx \alpha(\kappa^2 I - \Delta)^{{-s}}$  ($N={N_CELLS}$)"
    )
    ax_bessel.set_xlabel(r"depth $z$")
    ax_bessel.set_ylabel("model value")
    ax_bessel.legend(fontsize=10, loc="upper right")

    # (c) Eigenvalue decay
    ax_eval = fig.add_subplot(gs[1, :])
    j_idx = np.arange(1, N_CELLS + 1)
    ax_eval.semilogy(j_idx, naive_evals, "o--", color=PALETTE["naive"], lw=2.0,
                     ms=4, label=r"naive: $\sigma^2$ (flat)", alpha=0.8)
    ax_eval.semilogy(j_idx, bessel_evals, "s-", color=PALETTE["correct"], lw=2.2,
                     ms=4, label=r"Bessel: decaying eigenvalues")
    ax_eval.set_xlabel(r"eigenvalue index $j$")
    ax_eval.set_ylabel(r"eigenvalue $\lambda_j$")
    ax_eval.set_title("Prior covariance eigenvalue spectrum")
    ax_eval.legend(fontsize=11, loc="upper right")
    ax_eval.set_xlim(0.5, N_CELLS + 0.5)

    save(fig, "fig7a_corrected_prior", ps.output_dir())
    print("wrote fig7a_corrected_prior")


if __name__ == "__main__":
    main()
