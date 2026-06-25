"""Figure F2 - the naive hat-function Bayesian posterior mean.

Discretise with hat functions, place a naive sigma_m^2 I prior on the coefficients,
compute the Bayesian posterior mean, and overlay it on the truth. The mean tracks
the true model closely - nothing looks wrong yet.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import problem_setup as ps
from style import PALETTE, apply_style, plt, save

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

N_CELLS = 30


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

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    ax.plot(x, mean_func.evaluate(x), color=PALETTE["mako_dark"], lw=2.2,
            label=rf"posterior mean $\bar{{m}}_N^{{\tilde{{d}}}}(z)$ ($N={N_CELLS}$)")
    ax.set_title("Naive Bayesian posterior mean: looks fine")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig2_naive_hat", ps.output_dir())
    print("wrote fig2_naive_hat")


if __name__ == "__main__":
    main()
