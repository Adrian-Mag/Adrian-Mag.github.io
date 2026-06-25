"""Figure F7d - Trace comparison: naive vs corrected posterior.

Plots Tr(C_N^obs) for the naive prior and Tr(C_{0,N}^obs) for the Bessel
prior, across a range of N. Also shows the naive lower bound sigma^2(N-K).
The key visual: naive trace grows, corrected trace levels off.
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

N_VALUES = list(range(ps.N_D + 1, 51))  # 21..50


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    data_space = forward.codomain
    bessel_cov = ps.make_bessel_covariance(model_space)

    naive_traces = []
    bessel_traces = []

    for n in N_VALUES:
        box = ps.hat_coeff_space(n)
        data_err = ps.data_error_measure(data, data_space)

        # Naive
        naive_prior = ps.discrete_prior("naive", box)
        g_disc = LinearOperator.from_formal_adjoint(
            box.coeff_space, data_space,
            forward @ box.function_space.coordinate_inclusion,
        )
        problem = LinearForwardProblem(g_disc, data_error_measure=data_err)
        inv = LinearBayesianInversion(problem, naive_prior, formalism="data_space")
        post = inv.model_posterior_measure(data.d, CholeskySolver())
        naive_traces.append(float(np.trace(post.covariance.matrix(dense=True))))

        # Bessel
        bessel_prior = ps.discrete_prior("bessel", box, bessel_covariance=bessel_cov)
        problem2 = LinearForwardProblem(g_disc, data_error_measure=data_err)
        inv2 = LinearBayesianInversion(problem2, bessel_prior, formalism="data_space")
        post2 = inv2.model_posterior_measure(data.d, CholeskySolver())
        bessel_traces.append(float(np.trace(post2.covariance.matrix(dense=True))))

        print(f"  N={n}: naive Tr={naive_traces[-1]:.2f}  bessel Tr={bessel_traces[-1]:.2f}",
              flush=True)

    ns = np.array(N_VALUES)
    naive_traces = np.array(naive_traces)
    bessel_traces = np.array(bessel_traces)
    lower_bound = ps.NAIVE_SIGMA ** 2 * (ns - ps.N_D)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_yscale("log")
    ax.plot(ns, naive_traces, "o-", color=PALETTE["naive"], lw=2.4, ms=5,
            label=r"naive  $\operatorname{Tr}(\mathbf{C}_N^{\tilde{d}})$")
    ax.plot(ns, lower_bound, "--", color=PALETTE["true"], lw=1.8,
            label=rf"naive lower bound  $\sigma^2(N-K)$  ($\sigma={ps.NAIVE_SIGMA}$, $K={ps.N_D}$)")
    ax.plot(ns, bessel_traces, "s-", color=PALETTE["correct"], lw=2.4, ms=5,
            label=r"corrected  $\operatorname{Tr}(\mathbf{C}_{0,N}^{\tilde{d}})$")
    ax.fill_between(ns, lower_bound, naive_traces, alpha=0.08, color=PALETTE["naive"])
    ax.set_xlabel(r"number of basis functions $N$")
    ax.set_ylabel(r"posterior covariance trace  (log scale)")
    ax.set_title("Posterior trace: naive diverges, corrected converges")
    ax.legend(fontsize=11, loc="upper left")

    fig.tight_layout()
    save(fig, "fig7d_trace_comparison", ps.output_dir())
    print("wrote fig7d_trace_comparison")


if __name__ == "__main__":
    main()
