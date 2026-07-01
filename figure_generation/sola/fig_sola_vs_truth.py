"""Figure: SOLA estimates vs true target properties — the apparent failure.

Used in Act 7 (A Synthetic Cautionary Tale). Shows the SOLA estimates
with +/- 2*sigma bands alongside the true target properties T(m_bar).
The true values may lie far outside the propagated uncertainty bands
because the true model contains a high-frequency component invisible
to G but visible to T.
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

    X = prob.X_constrained_noisy
    p_tilde = ps.sola_estimates(X, prob.data)
    C_P = ps.propagated_covariance(X, prob.data)
    sigma = np.sqrt(np.diag(C_P))

    # True target properties (with the hidden high-freq component)
    p_bar = ps.true_target_properties(prob.target, prob.m_bar)

    # True target properties (smooth model — no hidden component)
    p_bar_smooth = ps.true_target_properties(prob.target, prob.m_bar_smooth)

    tc = ps.target_centers(ps.N_P)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Propagated uncertainty band
    ax.fill_between(tc, p_tilde - 2 * sigma, p_tilde + 2 * sigma,
                    color=PALETTE["data"], alpha=0.2, label=r"$\pm 2\sigma$ band")

    # SOLA estimates
    ax.plot(tc, p_tilde, "o", color=PALETTE["data"], ms=6,
            label=r"SOLA estimates $\tilde{\mathbf{p}}$")

    # True target properties (smooth — would be fine)
    ax.plot(tc, p_bar_smooth, "s", color=PALETTE["true"], ms=6, alpha=0.5,
            label=r"smooth truth $\mathcal{T}(\bar{m}_{\rm smooth})$")

    # True target properties (with hidden component — the failure)
    ax.plot(tc, p_bar, "D", color=PALETTE["naive"], ms=7, lw=2,
            label=r"actual truth $\mathcal{T}(\bar{m})$")

    ax.set_title(r"SOLA estimates vs true target properties: the apparent failure")
    ax.set_xlabel(r"target location $r_k$")
    ax.set_ylabel(r"property value")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper right", fontsize=10)

    fig.tight_layout()
    save(fig, "fig_sola_vs_truth", ps.output_dir())
    print("wrote fig_sola_vs_truth")


if __name__ == "__main__":
    main()
