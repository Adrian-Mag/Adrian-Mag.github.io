"""Figure F1c - the discretized forward matrix G.

A single panel showing the forward matrix [G]_{ij} as an imshow heatmap with
the mako colormap. Rows correspond to data indices, columns to basis function
indices.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save, FG

N_CELLS = 30


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)

    box = ps.hat_coeff_space(N_CELLS)
    data_space = forward.codomain

    # Build the discrete forward matrix
    from pygeoinf import LinearOperator
    g_discrete = LinearOperator.from_formal_adjoint(
        box.coeff_space, data_space,
        forward @ box.function_space.coordinate_inclusion,
    )
    g_mat = g_discrete.matrix(dense=True, galerkin=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(g_mat, aspect="auto", cmap=PALETTE["mako"],
                   origin="upper", interpolation="nearest")
    ax.set_title(rf"Discrete forward matrix $[\mathbf{{G}}]_{{ij}}$ ($N_d={ps.N_D}$, $N={N_CELLS}$)")
    ax.set_xlabel(r"basis index $j$")
    ax.set_ylabel(r"observation index $i$")
    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label(r"$[\mathbf{G}]_{ij}$", color=PALETTE.get("muted", FG))
    cbar.ax.tick_params(colors=PALETTE.get("muted", FG))

    fig.tight_layout()
    save(fig, "fig1c_gmatrix", ps.output_dir())
    print("wrote fig1c_gmatrix")


if __name__ == "__main__":
    main()
