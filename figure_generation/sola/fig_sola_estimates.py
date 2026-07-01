"""Figure: SOLA property estimates with propagated uncertainty.

Used in Act 5 (Noise Enters the Room) and Act 7 (A Synthetic Cautionary Tale).
Shows the SOLA estimates p_tilde_k with +/- 2*sigma error bars from
the propagated covariance C_P = X C_D X*.
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

    # Use constrained noisy SOLA
    X = prob.X_constrained_noisy
    p_tilde = ps.sola_estimates(X, prob.data)
    C_P = ps.propagated_covariance(X, prob.data)
    sigma = np.sqrt(np.diag(C_P))

    # Target centers for x-axis
    tc = ps.target_centers(ps.N_P)

    fig, ax = plt.subplots(figsize=(9, 4.5))

    ax.errorbar(tc, p_tilde, yerr=2 * sigma, fmt="o", color=PALETTE["data"],
                ms=7, capsize=4, lw=2, label=r"SOLA estimates $\tilde{\mathbf{p}} \pm 2\sigma$")
    ax.axhline(0, color=PALETTE["muted"], alpha=0.3, lw=1)

    ax.set_title(r"SOLA property estimates with propagated uncertainty")
    ax.set_xlabel(r"target location $r_k$")
    ax.set_ylabel(r"$[\tilde{\mathbf{p}}]_k$")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper right")

    fig.tight_layout()
    save(fig, "fig_sola_estimates", ps.output_dir())
    print("wrote fig_sola_estimates")


if __name__ == "__main__":
    main()
