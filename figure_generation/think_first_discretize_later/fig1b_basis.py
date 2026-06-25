"""Figure F1b - basis functions and discretized true model.

Two panels: (a) the hat basis functions at the chosen resolution, and (b) the
true model overlaid with its discretized (projected) approximation.
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

    # Project true model onto the basis: coefficients = coordinate_inclusion(m_bar)
    # Equivalently, evaluate hat functions at nodes for nodal interpolation.
    nodes = np.linspace(ps.DOMAIN[0], ps.DOMAIN[1], N_CELLS)
    coeffs = np.asarray(m_bar.evaluate(nodes), dtype=float)
    m_disc = fs.from_components(coeffs)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # (a) Hat basis functions — mako gradient
    ax = axes[0]
    colors = mako_light_n(N_CELLS)
    for j in range(N_CELLS):
        ax.plot(x, fs.get_basis_function(j).evaluate(x), color=colors[j],
                alpha=0.7, lw=1.5)
    ax.set_title(rf"(a) Hat basis functions ($N={N_CELLS}$)")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel(r"$\phi_j(z)$")

    # (b) True model vs discretized model
    ax = axes[1]
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6,
            label=r"true model $\bar{m}(z)$")
    ax.plot(x, m_disc.evaluate(x), color=PALETTE["mako_dark"], lw=2.2,
            linestyle="--", label=rf"discretized $m_N(z)$ ($N={N_CELLS}$)")
    ax.scatter(nodes, coeffs, color=PALETTE["mako_light"], s=30, zorder=5,
               label=r"coefficients $[\mathbf{u}]_j$")
    ax.set_title(r"(b) True model and its discretization")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig1b_basis", ps.output_dir())
    print("wrote fig1b_basis")


if __name__ == "__main__":
    main()
