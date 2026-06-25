"""Figure F7c - Corrected refinement slider data generator.

Pre-computes Bessel posterior mean and pointwise std at multiple resolutions N
for the corrected prior, and writes a JavaScript file for the interactive
slider in act-7.html. As N increases, the uncertainty should stabilize.

This mirrors fig2e_refinement_slider.py but uses the Bessel prior instead
of the naive sigma*I prior.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE  # noqa: F401  (ensures style module is importable)

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

N_VALUES = list(range(ps.N_D + 1, 51))  # 21..50, same as F2e
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

    results = {}
    for n in N_VALUES:
        box = ps.hat_coeff_space(n)
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

        mean_vals = np.asarray(
            box.function_space.from_components(posterior.expectation).evaluate(x),
            dtype=float,
        )

        samples = np.asarray(
            [np.asarray(box.function_space.from_components(
                posterior.sample()).evaluate(x), dtype=float)
             for _ in range(N_STD_SAMPLES)],
            dtype=float,
        )
        std_vals = samples.std(axis=0)

        results[str(n)] = {
            "mean": mean_vals.tolist(),
            "std": std_vals.tolist(),
        }
        print(f"  N={n}: mean range [{mean_vals.min():.3f}, {mean_vals.max():.3f}], "
              f"std range [{std_vals.min():.3f}, {std_vals.max():.3f}]", flush=True)

    output = {
        "x": x.tolist(),
        "true_model": m_true.tolist(),
        "posterior": results,
        "n_values": N_VALUES,
        "k": ps.N_D,
    }

    out_dir = ps.output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fig7c_refinement_data.js"
    with open(out_path, "w") as f:
        f.write("window.F7C_DATA = ")
        json.dump(output, f, separators=(",", ":"))
        f.write(";\n")

    print(f"wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
