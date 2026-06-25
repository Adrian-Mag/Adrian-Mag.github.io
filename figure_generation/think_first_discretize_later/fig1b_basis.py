"""Figure F1b - basis functions, coefficient vector, and discretized model.

Three panels: (a) the hat basis functions, (b) the coefficient vector of the
true model shown as a 1-row imshow strip (coefficient world), and (c) the true
model overlaid with its discretized reconstruction (function world).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save

N_CELLS = 30


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    x = ps.plot_grid()

    box = ps.hat_coeff_space(N_CELLS)
    fs = box.function_space

    nodes = np.linspace(ps.DOMAIN[0], ps.DOMAIN[1], N_CELLS)
    coeffs = np.asarray(m_bar.evaluate(nodes), dtype=float)
    m_disc = fs.from_components(coeffs)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.2),
                             gridspec_kw={"width_ratios": [1.2, 1.0, 1.2]})

    # (a) Hat basis functions — mako gradient
    ax = axes[0]
    colors = mako_light_n(N_CELLS)
    for j in range(N_CELLS):
        ax.plot(x, fs.get_basis_function(j).evaluate(x), color=colors[j],
                alpha=0.7, lw=1.5)
    ax.set_title(rf"(a) Hat basis functions ($N={N_CELLS}$)")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel(r"$\phi_j(z)$")

    # (b) Coefficient vector as 1-row imshow — coefficient world
    ax = axes[1]
    im = ax.imshow(coeffs.reshape(1, -1), aspect="auto", cmap=PALETTE["mako"],
                   origin="upper", interpolation="nearest")
    ax.set_title(r"(b) Coefficients $[\mathbf{u}]_j$")
    ax.set_xlabel(r"coefficient index $j$")
    ax.set_yticks([])
    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("coefficient value", color=PALETTE.get("muted", "#dce6f5"))
    cbar.ax.tick_params(colors=PALETTE.get("muted", "#dce6f5"))

    # (c) True model vs discretized model — function world
    ax = axes[2]
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    ax.plot(x, m_disc.evaluate(x), color=PALETTE["mako_dark"], lw=2.2,
            linestyle="--", label=rf"discretized $m_N(z)$ ($N={N_CELLS}$)")
    ax.set_title(r"(c) True model and its discretization")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig1b_basis", ps.output_dir())
    print("wrote fig1b_basis")


if __name__ == "__main__":
    main()
