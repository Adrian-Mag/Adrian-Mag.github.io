"""Figure: Target kernels T^(k) for the cautionary tale.

Used in Act 7 (A Synthetic Cautionary Tale). Shows the localised
averaging target kernels defining the property map T.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    target = ps.make_target(model_space)
    x = ps.plot_grid()

    fig, ax = plt.subplots(figsize=(8, 4.5))

    colors = mako_light_n(ps.N_P)
    for k in range(ps.N_P):
        tk = target.get_kernel(k)
        ax.plot(x, tk.evaluate(x), color=colors[k], alpha=0.7, lw=1.6)

    ax.set_title(r"Target kernels $\mathcal{T}_k(r)$")
    ax.set_xlabel(r"$r$")
    ax.set_ylabel("kernel value")
    ax.set_xlim(0, 1)

    fig.tight_layout()
    save(fig, "fig_target_kernels", ps.output_dir())
    print("wrote fig_target_kernels")


if __name__ == "__main__":
    main()
