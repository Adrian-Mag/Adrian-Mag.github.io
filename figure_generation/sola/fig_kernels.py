"""Figure: Sensitivity kernels K_i(r) on [0, 1].

Used in Act 1 (The Kernel Game) and Act 7 (A Synthetic Cautionary Tale).

Three-panel figure:
  1. A single kernel with annotations showing sensitive / insensitive regions.
  2. A second kernel with a different sensitivity pattern.
  3. All N_d kernels together — "a bunch of them, as in a real problem".
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save

# Kernels chosen for pedagogical contrast:
#   7  — strong oscillations, large insensitive region (~69%)
#   19 — gentler, even larger insensitive region (~76%)
_SINGLE_KERNELS = [7, 19]


def _shade_insensitive(ax, x, vals, threshold_frac: float = 0.15) -> None:
    """Shade regions where |K(r)| is small relative to the peak."""
    absmax = np.max(np.abs(vals))
    threshold = threshold_frac * absmax
    small = np.abs(vals) < threshold

    # Find contiguous runs of small values
    edges = np.where(np.diff(small.astype(int)) != 0)[0]
    if small[0]:
        edges = np.concatenate([[-1], edges])
    if small[-1]:
        edges = np.concatenate([edges, [len(small) - 1]])

    for j in range(0, len(edges), 2):
        lo = max(edges[j] + 1, 0)
        hi = min(edges[j + 1] + 1, len(x) - 1)
        ax.axvspan(x[lo], x[hi], color=PALETTE["muted"], alpha=0.12, zorder=0)


def _annotate_kernel(ax, x, vals, idx: int) -> None:
    """Add annotations pointing to sensitive and insensitive regions."""
    absmax = np.max(np.abs(vals))
    threshold = 0.15 * absmax

    # Find the most sensitive point (largest |K|)
    i_peak = np.argmax(np.abs(vals))
    r_peak = x[i_peak]

    # Find a contiguous insensitive region to annotate
    small = np.abs(vals) < threshold
    # Find the longest run of small values
    best_len = 0
    best_lo, best_hi = 0, 0
    edges = np.where(np.diff(small.astype(int)) != 0)[0]
    if small[0]:
        edges = np.concatenate([[-1], edges])
    if small[-1]:
        edges = np.concatenate([edges, [len(small) - 1]])
    for j in range(0, len(edges), 2):
        lo = max(edges[j] + 1, 0)
        hi = min(edges[j + 1] + 1, len(x) - 1)
        length = hi - lo
        if length > best_len:
            best_len = length
            best_lo, best_hi = lo, hi

    r_insens = (x[best_lo] + x[best_hi]) / 2

    # Annotate sensitive region
    # Keep the label INSIDE the axes: peaks sit at the extremes, so placing
    # the text beyond them overflows into the title / x-axis. Anchor it at
    # ~65% of the peak height instead and let the arrow bridge the gap.
    y_text = 0.65 * vals[i_peak]
    ax.annotate(
        r"data is sensitive here",
        xy=(r_peak, vals[i_peak]),
        xytext=(r_peak + 0.22, y_text),
        fontsize=10,
        color=PALETTE["true"],
        arrowprops=dict(arrowstyle="->", color=PALETTE["true"], lw=1.2),
        ha="left",
        va="center",
    )

    # Annotate insensitive region
    y_mid = 0
    ax.annotate(
        r"data is mostly insensitive here",
        xy=(r_insens, y_mid),
        xytext=(r_insens - 0.15, -absmax * 0.45),
        fontsize=10,
        color=PALETTE["muted"],
        arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.2),
        ha="center",
        va="top",
    )


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    x = ps.plot_grid()

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), gridspec_kw={"width_ratios": [1.1, 1.1, 1.4]})

    colors = mako_light_n(ps.N_D)

    # --- Panels 1 & 2: individual kernels with annotations ---
    for panel, idx in enumerate(_SINGLE_KERNELS):
        ax = axes[panel]
        ki = forward.get_kernel(idx)
        vals = ki.evaluate(x)

        _shade_insensitive(ax, x, vals)
        ax.plot(x, vals, color=colors[idx], alpha=0.9, lw=2.2)
        ax.axhline(0, color=PALETTE["muted"], alpha=0.4, lw=0.8)

        _annotate_kernel(ax, x, vals, idx)

        ax.set_title(rf"Kernel $K_{{{idx}}}(r)$")
        ax.set_xlabel(r"$r$")
        ax.set_ylabel("kernel value")
        ax.set_xlim(0, 1)

    # --- Panel 3: all kernels together ---
    ax = axes[2]
    for i in range(ps.N_D):
        ki = forward.get_kernel(i)
        ax.plot(x, ki.evaluate(x), color=colors[i], alpha=0.7, lw=1.4)

    ax.set_title(rf"All ${ps.N_D}$ sensitivity kernels $K_i(r)$")
    ax.set_xlabel(r"$r$")
    ax.set_xlim(0, 1)
    ax.set_yticks([])

    fig.tight_layout()
    save(fig, "fig_kernels", ps.output_dir())
    print("wrote fig_kernels")


if __name__ == "__main__":
    main()
