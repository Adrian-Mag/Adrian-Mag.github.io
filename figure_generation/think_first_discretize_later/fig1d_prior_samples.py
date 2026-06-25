"""Figure F1d - prior samples as coefficients and as function reconstructions.

Two panels: (a) samples from the naive prior (sigma^2 I) shown as coefficient
vectors, and (b) the same samples reconstructed as functions via the hat basis.
Also shows the prior mean (zero) and the true model for reference.
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
SIGMA = ps.NAIVE_SIGMA


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    x = ps.plot_grid()

    box = ps.hat_coeff_space(N_CELLS)
    fs = box.function_space

    # Draw coefficient samples from the naive prior: u ~ N(0, sigma^2 I_N)
    rng = np.random.default_rng(42)
    coeff_samples = rng.normal(0.0, SIGMA, size=(N_SAMPLES, N_CELLS))

    # Reconstruct functions from coefficients
    func_samples = np.asarray(
        [np.asarray(fs.from_components(c).evaluate(x), dtype=float)
         for c in coeff_samples],
        dtype=float,
    )

    nodes = np.linspace(ps.DOMAIN[0], ps.DOMAIN[1], N_CELLS)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # (a) Coefficient samples
    ax = axes[0]
    colors = mako_light_n(N_SAMPLES)
    for s in range(N_SAMPLES):
        ax.plot(np.arange(N_CELLS), coeff_samples[s], color=colors[s],
                alpha=0.7, lw=1.5, marker="o", ms=3)
    ax.axhline(0, color=PALETTE["muted"], lw=1.5, linestyle="--",
               label=r"prior mean $0$")
    ax.set_title(rf"(a) Prior coefficient samples $[\mathbf{{u}}]_j$ ($\sigma={SIGMA}$, $N={N_CELLS}$)")
    ax.set_xlabel(r"coefficient index $j$")
    ax.set_ylabel("coefficient value")
    ax.legend()

    # (b) Function reconstructions
    ax = axes[1]
    for s in range(N_SAMPLES):
        ax.plot(x, func_samples[s], color=colors[s], alpha=0.5, lw=1.2)
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    ax.axhline(0, color=PALETTE["muted"], lw=1.5, linestyle="--",
               label="prior mean $0$")
    ax.set_title(rf"(b) Reconstructed prior samples $m_N^{{(s)}}(z)$ ($n={N_SAMPLES}$)")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig1d_prior_samples", ps.output_dir())
    print("wrote fig1d_prior_samples")


if __name__ == "__main__":
    main()
