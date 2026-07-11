"""Figure F1d - prior samples as coefficients and as function reconstructions.

Two panels: (a) samples from the naive prior (sigma^2 i) shown as an imshow
heatmap (rows = samples, columns = coefficient indices — coefficient world),
and (b) the same samples reconstructed as functions via the hat basis
(function world). Also shows the true model for reference.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save, FG

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

    rng = np.random.default_rng(42)
    coeff_samples = rng.normal(0.0, SIGMA, size=(N_SAMPLES, N_CELLS))

    func_samples = np.asarray(
        [np.asarray(fs.from_components(c).evaluate(x), dtype=float)
         for c in coeff_samples],
        dtype=float,
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1.0, 1.3]})

    # (a) Coefficient samples as imshow — coefficient world
    ax = axes[0]
    im = ax.imshow(coeff_samples, aspect="auto", cmap=PALETTE["mako"],
                   origin="upper", interpolation="nearest")
    ax.set_title(rf"(a) Prior coefficient samples $[\mathbf{{u}}^{{(s)}}]_j$ ($\sigma={SIGMA}$)")
    ax.set_xlabel(r"coefficient index $j$")
    ax.set_ylabel(r"sample index $s$")
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("coefficient value", color=PALETTE.get("muted", FG))
    cbar.ax.tick_params(colors=PALETTE.get("muted", FG))

    # (b) Function reconstructions — function world
    ax = axes[1]
    colors = mako_light_n(N_SAMPLES)
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
