"""Export ``discretization_sweep.json`` for the Act 2 interactive panel.

For each resolution N, stores the naive posterior mean and several posterior
sample curves (not just std), so the web page can show actual sample paths
alongside the mean as the user sweeps N.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps

from pygeoinf import CholeskySolver, LinearOperator
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

DOWNSAMPLE = 4       # keep every 4th grid point to shrink payload
ROUND = 4
N_SAMPLES = 10       # sample curves per N
NS: tuple[int, ...] = (10, 15, 20, 25, 30, 35, 40, 45, 50)


def _round(array: np.ndarray) -> list[float]:
    return [round(float(v), ROUND) for v in array]


def _posterior_mean_and_samples(
    forward, data, box, x, n_samples
):
    """Compute naive posterior mean and sample curves on the plotting grid."""
    data_space = forward.codomain
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

    mean = np.asarray(
        box.function_space.from_components(posterior.expectation).evaluate(x), float
    )
    samples = np.asarray(
        [np.asarray(box.function_space.from_components(posterior.sample()).evaluate(x), float)
         for _ in range(n_samples)],
        dtype=float,
    )
    return mean, samples


def main() -> None:
    np.random.seed(0)
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    x = ps.plot_grid()
    x_ds = x[::DOWNSAMPLE]
    true_vals = np.asarray(m_bar.evaluate(x), dtype=float)

    naive: dict[str, dict] = {}
    rms_std: list[float] = []

    for n in NS:
        print(f"  N={n}...", flush=True)
        box = ps.hat_coeff_space(n)
        mean_full, samples_full = _posterior_mean_and_samples(
            forward, data, box, x, N_SAMPLES
        )
        mean_ds = mean_full[::DOWNSAMPLE]
        samples_ds = samples_full[:, ::DOWNSAMPLE]
        std = samples_full.std(axis=0)
        naive[str(n)] = {
            "mean": _round(mean_ds),
            "samples": [_round(s) for s in samples_ds],
        }
        rms_std.append(float(np.sqrt(np.mean(std ** 2))))

    payload = {
        "x": _round(x_ds),
        "true": _round(true_vals[::DOWNSAMPLE]),
        "ns": list(NS),
        "naive": naive,
        "summary": {
            "ns": list(NS),
            "naive_rms_std": [round(v, ROUND) for v in rms_std],
        },
        "meta": {
            "domain": list(ps.DOMAIN),
            "n_data": ps.N_D,
            "naive_sigma": ps.NAIVE_SIGMA,
            "n_samples": N_SAMPLES,
        },
    }

    out_path = ps.output_dir() / "discretization_sweep.json"
    out_path.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"wrote {out_path}  ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
