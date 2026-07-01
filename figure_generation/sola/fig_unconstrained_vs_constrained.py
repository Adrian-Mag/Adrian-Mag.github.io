"""Figure: Unconstrained vs constrained resolving kernel.

Used in Act 3 (Averages Need Mass). Shows the unconstrained resolving
kernel and the constrained resolving kernel side by side, highlighting
that the constrained version has unit area even if its shape changes.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save


def main() -> None:
    apply_style()
    prob = ps.make_problem()
    x = prob.x

    # Show a few kernels at different locations
    ks = [0, ps.N_P // 4, ps.N_P // 2, 3 * ps.N_P // 4, ps.N_P - 1]

    fig, axes = plt.subplots(1, len(ks), figsize=(16, 3.5), sharey=True)

    for idx, k in enumerate(ks):
        ax = axes[idx]
        rk_unc = ps.resolving_kernel(prob.forward, prob.X_noisy, k, x)
        rk_con = ps.resolving_kernel(prob.forward, prob.X_constrained_noisy, k, x)
        tk = ps.target_kernel_eval(prob.target, k, x)

        mass_unc = np.trapezoid(rk_unc, x)
        mass_con = np.trapezoid(rk_con, x)

        ax.plot(x, rk_unc, color=PALETTE["naive"], lw=2.0, alpha=0.7,
                label=rf"unconstrained (mass={mass_unc:.2f})")
        ax.plot(x, rk_con, color=PALETTE["correct"], lw=2.5,
                label=rf"constrained (mass={mass_con:.2f})")
        ax.plot(x, tk, color=PALETTE["correct"], lw=1.5, ls="--", alpha=0.4)
        ax.set_title(rf"$k={k}$", fontsize=12)
        ax.set_xlabel(r"$r$")
        if idx == 0:
            ax.set_ylabel("kernel value")
        ax.set_xlim(0, 1)

    axes[-1].legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    save(fig, "fig_unconstrained_vs_constrained", ps.output_dir())
    print("wrote fig_unconstrained_vs_constrained")


if __name__ == "__main__":
    main()
