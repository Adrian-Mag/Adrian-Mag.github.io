"""Figure: Resolving kernels overlaid on target kernels (good match).

Used in Act 7 (A Synthetic Cautionary Tale). Shows resolving kernels
R_k overlaid on target kernels T^(k). The visual match should look
good — this is the "standard diagnostics look fine" panel.
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

    X = prob.X_constrained_noisy

    # Show a representative subset
    ks = [1, ps.N_P // 3, ps.N_P // 2, 2 * ps.N_P // 3, ps.N_P - 2]

    fig, axes = plt.subplots(1, len(ks), figsize=(16, 3.5), sharey=True)

    for idx, k in enumerate(ks):
        ax = axes[idx]
        rk = ps.resolving_kernel(prob.forward, X, k, x)
        tk = ps.target_kernel_eval(prob.target, k, x)

        ax.plot(x, rk, color=PALETTE["mako_dark"], lw=2.5,
                label=r"$R_k(r)$")
        ax.plot(x, tk, color=PALETTE["correct"], lw=2.0, ls="--",
                label=r"$\mathcal{T}_k(r)$")
        ax.fill_between(x, 0, rk, color=PALETTE["mako_dark"], alpha=0.1)
        ax.set_title(rf"$k={k}$", fontsize=12)
        ax.set_xlabel(r"$r$")
        if idx == 0:
            ax.set_ylabel("kernel value")
        ax.set_xlim(0, 1)

    axes[-1].legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    save(fig, "fig_resolving_vs_target", ps.output_dir())
    print("wrote fig_resolving_vs_target")


if __name__ == "__main__":
    main()
