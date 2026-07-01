"""Figure: Weighted sensitivity kernels forming a resolving kernel.

Used in Act 2 (Building SOLA from Scratch). Shows several sensitivity
kernels K_i with their weights x_i, and the resulting resolving kernel
R_x = sum_i x_i K_i overlaid with the target kernel T^(1).
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
    prob = ps.make_problem()
    x = prob.x

    fig, ax = plt.subplots(figsize=(9, 5))

    # Pick a target index near the middle
    k = ps.N_P // 2

    # Show the sensitivity kernels with their SOLA weights
    weights = prob.X_noiseless[k, :]
    colors = mako_light_n(ps.N_D)
    for i in range(ps.N_D):
        ki = prob.forward.get_kernel(i)
        ax.plot(x, ki.evaluate(x), color=colors[i], alpha=0.3, lw=1.2)

    # Resolving kernel
    rk = ps.resolving_kernel(prob.forward, prob.X_noiseless, k, x)
    ax.plot(x, rk, color=PALETTE["mako_dark"], lw=2.8,
            label=r"resolving kernel $R_k(r)$")

    # Target kernel
    tk = ps.target_kernel_eval(prob.target, k, x)
    ax.plot(x, tk, color=PALETTE["correct"], lw=2.5, ls="--",
            label=r"target kernel $\mathcal{T}_k(r)$")

    ax.set_title(r"Weighted kernels become a resolving kernel")
    ax.set_xlabel(r"$r$")
    ax.set_ylabel("kernel value")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper right")

    fig.tight_layout()
    save(fig, "fig_weighted_kernels", ps.output_dir())
    print("wrote fig_weighted_kernels")


if __name__ == "__main__":
    main()
