"""Figure F7b - Corrected posterior samples on hats.

Same visual grammar as F2b: true model, posterior mean, posterior samples,
and a ±1σ band. Uses the Bessel/operator prior so the posterior cloud
is controlled — "the posterior has stopped screaming."
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
    prior = ps.discrete_prior("bessel", box, bessel_covariance=bessel_cov)

    g_discrete = LinearOperator.from_formal_adjoint(
        box.coeff_space, data_space,
        forward @ box.function_space.coordinate_inclusion,
    )
    problem = LinearForwardProblem(
        g_discrete, data_error_measure=ps.data_error_measure(data, data_space),
    )
    inversion = LinearBayesianInversion(problem, prior, formalism="data_space")
    posterior = inversion.model_posterior_measure(data.d, CholeskySolver())

    mean_func = box.function_space.from_components(posterior.expectation)
    mean_vals = np.asarray(mean_func.evaluate(x), dtype=float)

    coeff_samples = np.asarray(
        [np.asarray(posterior.sample(), dtype=float) for _ in range(N_SAMPLES)],
        dtype=float,
    )
    sample_curves = np.asarray(
        [np.asarray(box.function_space.from_components(c).evaluate(x), float)
         for c in coeff_samples],
        dtype=float,
    )

    # Compute std from more samples for a smooth band
    n_std_samples = 200
    std_samples = np.asarray(
        [np.asarray(box.function_space.from_components(
            posterior.sample()).evaluate(x), dtype=float)
         for _ in range(n_std_samples)],
        dtype=float,
    )
    std_vals = std_samples.std(axis=0)

    fig, ax = plt.subplots(figsize=(10, 6))

    # ±1σ band
    ax.fill_between(x, mean_vals - std_vals, mean_vals + std_vals,
                    color=PALETTE["correct"], alpha=0.15, label=r"$\pm 1\sigma$ band")

    # Samples
    colors = mako_light_n(N_SAMPLES)
    for idx_s, s in enumerate(sample_curves):
        ax.plot(x, s, color=colors[idx_s], alpha=0.35, lw=1.0)

    # Mean and true
    ax.plot(x, mean_vals, color=PALETTE["correct"], lw=2.4,
            label=r"posterior mean $m_N^{\tilde{d}}(z)$")
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    ax.plot([], [], color=PALETTE["mako_mid"], alpha=0.35, lw=1.0,
            label=f"posterior samples (n={N_SAMPLES})")

    ax.set_title(rf"Corrected posterior: Bessel prior, $N={N_CELLS}$ hats, $N_d={ps.N_D}$ data")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend(fontsize=11, loc="upper right")

    fig.tight_layout()
    save(fig, "fig7b_corrected_posterior_samples", ps.output_dir())
    print("wrote fig7b_corrected_posterior_samples")


if __name__ == "__main__":
    main()
