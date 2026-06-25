"""Figure F4 - posterior stability under refinement (mirrors EGU poster fig10).

The same Bayesian inversion is run on a hat-function coefficient space at increasing
resolution N, with two priors: the naive Euclidean ``sigma^2 I`` and a
trace-class Bessel-Sobolev smoothing covariance. Top row (naive) shows the
posterior +/-2 sigma band exploding as N grows; the middle row (Bessel) stays
bounded and tracks the truth. The bottom panel quantifies it: max posterior std
vs N - naive diverges, Bessel converges.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save

NS_PLOT = (10, 50)


def _draw_band(ax, curves: "ps.PosteriorCurves", true_vals, color, title) -> None:
    ax.fill_between(curves.x, curves.mean - 2 * curves.std, curves.mean + 2 * curves.std,
                    color=color, alpha=0.18, label=r"posterior $\pm2\sigma$")
    ax.plot(curves.x, curves.mean, color=color, lw=2.2, label="posterior mean")
    ax.plot(curves.x, true_vals, color=PALETTE["true"], lw=1.8, ls=":", label="true model")
    ax.set_title(title)


def main() -> None:
    apply_style()
    result = ps.compute_refinement()
    x, true_vals = result.x, result.true_vals

    fig = plt.figure(figsize=(13, 11))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 1.05], hspace=0.4, wspace=0.16)

    ax_n10 = fig.add_subplot(gs[0, 0])
    ax_n50 = fig.add_subplot(gs[0, 1], sharey=ax_n10)
    ax_b10 = fig.add_subplot(gs[1, 0])
    ax_b50 = fig.add_subplot(gs[1, 1], sharey=ax_b10)

    _draw_band(ax_n10, result.naive[10], true_vals, PALETTE["naive"],
               r"Naive  $\sigma^2 I$  -  N=10 hats")
    _draw_band(ax_n50, result.naive[50], true_vals, PALETTE["naive"],
               r"Naive  $\sigma^2 I$  -  N=50 hats")
    _draw_band(ax_b10, result.bessel[10], true_vals, PALETTE["correct"],
               r"Bessel (trace-class)  -  N=10 hats")
    _draw_band(ax_b50, result.bessel[50], true_vals, PALETTE["correct"],
               r"Bessel (trace-class)  -  N=50 hats")

    ax_n10.set_ylabel("model value")
    ax_b10.set_ylabel("model value")
    ax_n10.legend(loc="upper right", fontsize=9)
    for ax in (ax_b10, ax_b50):
        ax.set_xlabel(r"depth $z$")

    ax_sum = fig.add_subplot(gs[2, :])
    ns = np.array(result.ns)
    rms = lambda c: float(np.sqrt(np.mean(c.std ** 2)))
    naive_rms = [rms(result.naive[n]) for n in result.ns]
    bessel_rms = [rms(result.bessel[n]) for n in result.ns]
    ax_sum.plot(ns, naive_rms, "o-", color=PALETTE["naive"], lw=2.4,
                label=r"naive $\sigma^2 I$ (diverges)")
    ax_sum.plot(ns, bessel_rms, "s-", color=PALETTE["correct"], lw=2.4,
                label="Bessel (converges)")
    ax_sum.set_xlabel(r"resolution $N$ (number of hats)")
    ax_sum.set_ylabel("RMS posterior std")
    ax_sum.set_title("Posterior uncertainty vs refinement")
    ax_sum.legend(loc="upper left")

    save(fig, "fig4_refinement", ps.output_dir())
    print("wrote fig4_refinement")


if __name__ == "__main__":
    main()
