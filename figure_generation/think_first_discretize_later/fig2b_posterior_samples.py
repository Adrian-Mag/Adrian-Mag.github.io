"""Figure F2b - posterior mean + samples on hats, revealing large spread.

Same setup as F2 (naive sigma_m^2 I prior, hat basis), but now we draw
samples from the posterior. The mean still tracks the truth, but the samples
reveal a surprisingly large spread.
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

    box = ps.hat_coeff_space(N_CELLS)
    prior = ps.discrete_prior("naive", box)
    data_space = forward.codomain

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
    sample_curves = np.asarray(
        [np.asarray(box.function_space.from_components(posterior.sample()).evaluate(x), float)
         for _ in range(N_SAMPLES)],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    sample_colors = mako_light_n(N_SAMPLES)
    for idx_s, s in enumerate(sample_curves):
        ax.plot(x, s, color=sample_colors[idx_s], alpha=0.3, lw=1.0)
    ax.plot(x, mean_func.evaluate(x), color=PALETTE["mako_dark"], lw=2.2,
            label=rf"posterior mean $\bar{{m}}_N^{{\tilde{{d}}}}(z)$ ($N={N_CELLS}$)")
    ax.plot([], [], color=PALETTE["mako_mid"], alpha=0.3, lw=1.0,
            label=f"posterior samples (n={N_SAMPLES})")
    ax.set_title("Naive Bayesian posterior: the mean looks fine, the samples do not")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig2b_posterior_samples", ps.output_dir())
    print("wrote fig2b_posterior_samples")


if __name__ == "__main__":
    main()
