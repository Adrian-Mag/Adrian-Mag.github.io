"""Figure F2d - total posterior variance vs number of basis functions.

Shows that Tr(C_N^obs) grows linearly with N for the naive prior (sigma^2 I),
while the lower bound sigma^2(N-K) is also plotted for reference. Uses
pygeoinf's LinearBayesianInversion to compute the posterior covariance at each
resolution.
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

# Sweep N from K+1 to N_MAX
N_MAX = 50
N_VALUES = list(range(ps.N_D + 1, N_MAX + 1))


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    data_space = forward.codomain

    sigma = ps.NAIVE_SIGMA
    K = ps.N_D

    traces = []
    for n in N_VALUES:
        box = ps.hat_coeff_space(n)
        prior = ps.discrete_prior("naive", box)

        g_discrete = LinearOperator.from_formal_adjoint(
            box.coeff_space, data_space,
            forward @ box.function_space.coordinate_inclusion,
        )
        problem = LinearForwardProblem(
            g_discrete, data_error_measure=ps.data_error_measure(data, data_space),
        )
        inversion = LinearBayesianInversion(problem, prior, formalism="data_space")
        posterior = inversion.model_posterior_measure(data.d, CholeskySolver())

        # Trace of posterior covariance in coefficient space
        cov_mat = posterior.covariance.matrix(dense=True)
        traces.append(float(np.trace(cov_mat)))

    traces = np.array(traces)
    ns = np.array(N_VALUES)
    lower_bound = sigma**2 * (ns - K)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(ns, traces, "o-", color=PALETTE["mako_dark"], lw=2.2, ms=5,
            label=r"$\operatorname{Tr}(\mathbf{C}_N^{\tilde{\mathbf{d}}})$ (naive prior)")
    ax.plot(ns, lower_bound, "--", color=PALETTE["true"], lw=2.0,
            label=rf"lower bound $\sigma^2(N - K)$ ($\sigma={sigma}$, $K={K}$)")
    ax.fill_between(ns, lower_bound, traces, alpha=0.12, color=PALETTE["mako_dark"])
    ax.set_xlabel(r"number of basis functions $N$")
    ax.set_ylabel(r"total posterior variance $\operatorname{Tr}(\mathbf{C}_N^{\tilde{\mathbf{d}}})$")
    ax.set_title("Total posterior variance grows with mesh refinement")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig2d_variance_growth", ps.output_dir())
    print(f"wrote fig2d_variance_growth (N={N_VALUES[0]}..{N_VALUES[-1]})")


if __name__ == "__main__":
    main()
