"""Figure F8c - Naive vs corrected refinement slider data generator.

Pre-computes both naive and Bessel posterior mean and pointwise std at
multiple resolutions N, and writes a JavaScript file for the interactive
dual-panel slider in act-8.html. As the slider moves, the left (naive)
panel inflates while the right (corrected) panel settles.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE  # noqa: F401

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

N_VALUES = list(range(ps.N_D + 1, 51))  # 21..50
N_GRID = 200
N_STD_SAMPLES = 100


def main() -> None:
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    data_space = forward.codomain
    bessel_cov = ps.make_bessel_covariance(model_space)
    x = np.linspace(ps.DOMAIN[0], ps.DOMAIN[1], N_GRID)
    m_true = np.asarray(m_bar.evaluate(x), dtype=float)

    naive_results = {}
    bessel_results = {}

    for n in N_VALUES:
        box = ps.hat_coeff_space(n)
        data_err = ps.data_error_measure(data, data_space)
        g_disc = LinearOperator.from_formal_adjoint(
            box.coeff_space, data_space,
            forward @ box.function_space.coordinate_inclusion,
        )

        # Naive
        naive_prior = ps.discrete_prior("naive", box)
        problem1 = LinearForwardProblem(g_disc, data_error_measure=data_err)
        inv1 = LinearBayesianInversion(problem1, naive_prior, formalism="data_space")
        post1 = inv1.model_posterior_measure(data.d, CholeskySolver())
        naive_mean = np.asarray(
            box.function_space.from_components(post1.expectation).evaluate(x), float)
        naive_samples = np.asarray(
            [np.asarray(box.function_space.from_components(
                post1.sample()).evaluate(x), float)
             for _ in range(N_STD_SAMPLES)],
            dtype=float,
        )
        naive_std = naive_samples.std(axis=0)
        naive_results[str(n)] = {
            "mean": naive_mean.tolist(),
            "std": naive_std.tolist(),
        }

        # Bessel
        bessel_prior = ps.discrete_prior("bessel", box, bessel_covariance=bessel_cov)
        problem2 = LinearForwardProblem(g_disc, data_error_measure=data_err)
        inv2 = LinearBayesianInversion(problem2, bessel_prior, formalism="data_space")
        post2 = inv2.model_posterior_measure(data.d, CholeskySolver())
        bessel_mean = np.asarray(
            box.function_space.from_components(post2.expectation).evaluate(x), float)
        bessel_samples = np.asarray(
            [np.asarray(box.function_space.from_components(
                post2.sample()).evaluate(x), float)
             for _ in range(N_STD_SAMPLES)],
            dtype=float,
        )
        bessel_std = bessel_samples.std(axis=0)
        bessel_results[str(n)] = {
            "mean": bessel_mean.tolist(),
            "std": bessel_std.tolist(),
        }

        print(f"  N={n}: naive max-std={naive_std.max():.3f}  "
              f"bessel max-std={bessel_std.max():.3f}", flush=True)

    output = {
        "x": x.tolist(),
        "true_model": m_true.tolist(),
        "naive": naive_results,
        "bessel": bessel_results,
        "n_values": N_VALUES,
        "k": ps.N_D,
    }

    out_dir = ps.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fig8c_refinement_data.js"
    with open(out_path, "w") as f:
        f.write("window.F8C_DATA = ")
        json.dump(output, f, separators=(",", ":"))
        f.write(";\n")

    print(f"wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
