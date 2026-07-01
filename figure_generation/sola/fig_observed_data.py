"""Figure: Observed data with error bars.

Used in Act 7 (A Synthetic Cautionary Tale). Shows the observed data
d_tilde with +/- 1*sigma error bars from the data covariance C_D.
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

    idx = np.arange(ps.N_D)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Noise-free data (hidden truth)
    ax.plot(idx, prob.data.d_clean, color=PALETTE["true"], marker="x",
            ls="", ms=8, lw=2.5, label=r"noise-free $\bar{\mathbf{d}}=G\bar{m}$")

    # Noisy data with error bars
    ax.errorbar(idx, prob.data.d, yerr=prob.data.noise_std, fmt="o",
                color=PALETTE["data"], ms=7, capsize=3, lw=1.8,
                label=r"observed $\tilde{\mathbf{d}} \pm 1\sigma$")

    ax.set_title(r"Observed data $\tilde{\mathbf{d}}$ with measurement uncertainty")
    ax.set_xlabel(r"observation index $i$")
    ax.set_ylabel(r"$[\tilde{\mathbf{d}}]_i$")
    ax.legend(loc="upper right")

    fig.tight_layout()
    save(fig, "fig_observed_data", ps.output_dir())
    print("wrote fig_observed_data")


if __name__ == "__main__":
    main()
