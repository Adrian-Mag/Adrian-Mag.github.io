"""Figure F2b - posterior mean + samples on hats, revealing large spread.

Two panels: (a) posterior coefficient samples as an imshow heatmap (rows =
samples, columns = coefficient indices — coefficient world), and (b) the same
samples reconstructed as functions (function world). The mean still tracks the
truth, but the samples reveal a surprisingly large spread.
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
    mean_coeffs = posterior.expectation
    coeff_samples = np.asarray(
        [np.asarray(posterior.sample(), dtype=float) for _ in range(N_SAMPLES)],
        dtype=float,
    )
    sample_curves = np.asarray(
        [np.asarray(box.function_space.from_components(c).evaluate(x), float)
         for c in coeff_samples],
        dtype=float,
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1.0, 1.3]})

    # (a) Coefficient samples as imshow — coefficient world
    ax = axes[0]
    all_coeffs = np.vstack([mean_coeffs.reshape(1, -1), coeff_samples])
    im = ax.imshow(all_coeffs, aspect="auto", cmap=PALETTE["mako"],
                   origin="upper", interpolation="nearest")
    ax.axhline(0.5, color=PALETTE["true"], lw=2.0, linestyle="-")
    ax.set_title(rf"(a) Posterior coefficient samples $[\mathbf{{u}}^{{(s)}}]_j$ ($N={N_CELLS}$)")
    ax.set_xlabel(r"coefficient index $j$")
    ax.set_ylabel(r"sample index $s$")
    ax.set_yticks([0])
    ax.set_yticklabels([r"mean"])
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("coefficient value", color=PALETTE.get("muted", "#dce6f5"))
    cbar.ax.tick_params(colors=PALETTE.get("muted", "#dce6f5"))

    # (b) Function reconstructions — function world
    ax = axes[1]
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    sample_colors = mako_light_n(N_SAMPLES)
    for idx_s, s in enumerate(sample_curves):
        ax.plot(x, s, color=sample_colors[idx_s], alpha=0.3, lw=1.0)
    ax.plot(x, mean_func.evaluate(x), color=PALETTE["mako_dark"], lw=2.2,
            label=rf"posterior mean $\tilde{{m}}_N^{{\tilde{{d}}}}(z)$ ($N={N_CELLS}$)")
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
