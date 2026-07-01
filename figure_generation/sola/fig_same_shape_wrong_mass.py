"""Figure: Two kernels with similar shape but different total mass.

Used in Act 3 (Averages Need Mass). Shows an unconstrained resolving
kernel (mass != 1) and a constrained resolving kernel (mass = 1) that
look visually similar but carry different averaging meaning.
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

    k = 2

    # Unconstrained (plain) resolving kernel — computed via intervalinf
    rk_unc = ps.resolving_kernel(prob.forward, prob.X_noiseless, k, x)
    mass_unc = np.trapezoid(rk_unc, x)

    # Constrained (unimodular) resolving kernel — computed via intervalinf
    rk_con = ps.resolving_kernel(prob.forward, prob.X_constrained_noiseless, k, x)
    mass_con = np.trapezoid(rk_con, x)

    # Target kernel
    tk = ps.target_kernel_eval(prob.target, k, x)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(x, tk, color=PALETTE["muted"], lw=2.0, ls="--",
            label=r"target $T_k$ (mass=1)")
    ax.plot(x, rk_unc, color=PALETTE["naive"], lw=2.5,
            label=rf"unconstrained $R_k$ (mass={mass_unc:.2f})")
    ax.plot(x, rk_con, color=PALETTE["correct"], lw=2.5,
            label=rf"constrained $R_k$ (mass={mass_con:.2f})")

    ax.fill_between(x, 0, rk_unc, color=PALETTE["naive"], alpha=0.08)
    ax.fill_between(x, 0, rk_con, color=PALETTE["correct"], alpha=0.08)

    ax.set_xlabel(r"$r$")
    ax.set_ylabel("kernel value")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper right")

    fig.tight_layout()
    save(fig, "fig_same_shape_wrong_mass", ps.output_dir())
    print("wrote fig_same_shape_wrong_mass")


if __name__ == "__main__":
    main()
