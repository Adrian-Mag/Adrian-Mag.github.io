"""Figure: SOLA map values with resolving kernels beneath each point.

Used in Act 6 (What Did SOLA Actually Estimate?). Shows a row of SOLA
map values with the corresponding resolving kernel R_k(r) shown beneath
each point, conveying that a SOLA map is a map of values plus a map of kernels.
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
    p_tilde = ps.sola_estimates(X, prob.data)
    C_P = ps.propagated_covariance(X, prob.data)
    sigma = np.sqrt(np.diag(C_P))
    tc = ps.target_centers(ps.N_P)

    fig = plt.figure(figsize=(14, 6))

    # Top panel: map values with error bars
    ax_top = fig.add_axes([0.06, 0.55, 0.90, 0.38])
    ax_top.errorbar(tc, p_tilde, yerr=2 * sigma, fmt="o", color=PALETTE["data"],
                    ms=6, capsize=3, lw=1.8,
                    label=r"$\tilde{\mathbf{p}} \pm 2\sigma$")
    ax_top.axhline(0, color=PALETTE["muted"], alpha=0.3, lw=1)
    ax_top.set_ylabel(r"$[\tilde{\mathbf{p}}]_k$")
    ax_top.set_xlim(0, 1)
    ax_top.set_xticklabels([])
    ax_top.legend(loc="upper right", fontsize=10)
    ax_top.set_title("A SOLA map is a map of values plus a map of kernels")

    # Bottom panel: resolving kernels, each coloured by its map location
    ax_bot = fig.add_axes([0.06, 0.08, 0.90, 0.42], sharex=ax_top)
    colors = mako_light_n(ps.N_P)
    for k in range(ps.N_P):
        rk = ps.resolving_kernel(prob.forward, X, k, x)
        ax_bot.plot(x, rk + tc[k] * 0, color=colors[k], alpha=0.5, lw=1.0)
        # Mark the centre
        ax_bot.axvline(tc[k], color=colors[k], alpha=0.15, lw=0.8)

    ax_bot.set_xlabel(r"$r$")
    ax_bot.set_ylabel(r"$R_k(r)$")
    ax_bot.set_xlim(0, 1)

    save(fig, "fig_map_with_kernels", ps.output_dir())
    print("wrote fig_map_with_kernels")


if __name__ == "__main__":
    main()
