"""Figure: Compact support vs Gaussian clipping on an interval.

Used in Act 4 (Beyond Averages). Shows three Gaussian target kernels at
different positions on [0,1] — one in the interior, one near the left
edge, one near the right edge — to illustrate that clipping changes the
effective target. Below, a compact-support (bump) target placed at the
same edge positions shows no clipping at all.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save, FG

_FG = FG


def _gaussian(r, r0, width):
    """Unnormalised Gaussian."""
    return np.exp(-((r - r0) / width) ** 2)


def _bump_compact(r, r0, width):
    r"""Smooth compact-support bump (C^\infty) on [r0-width, r0+width]."""
    u = (r - r0) / width
    vals = np.zeros_like(r)
    mask = np.abs(u) < 1.0
    vals[mask] = np.exp(-1.0 / (1.0 - u[mask] ** 2))
    return vals


def main() -> None:
    apply_style()
    x = ps.plot_grid()
    width = 0.08

    positions = [0.5, 0.12, 0.88]
    pos_labels = ["interior", "near left edge", "near right edge"]

    fig, axes = plt.subplots(2, 3, figsize=(14, 6), sharex=True, sharey="row")

    for idx, (r0, lab) in enumerate(zip(positions, pos_labels)):
        # Top row: Gaussian — gets clipped near edges
        ax = axes[0, idx]
        g = _gaussian(x, r0, width)
        mass = np.trapezoid(g, x)
        ax.plot(x, g, color=PALETTE["naive"], lw=2.5)
        ax.fill_between(x, 0, g, color=PALETTE["naive"], alpha=0.15)
        ax.axvline(0, color=PALETTE["muted"], lw=0.8, ls=":", alpha=0.6)
        ax.axvline(1, color=PALETTE["muted"], lw=0.8, ls=":", alpha=0.6)
        ax.set_title(f"Gaussian, {lab}\n(mass = {mass:.2f})", fontsize=11)
        ax.set_xlim(-0.05, 1.05)
        if idx == 0:
            ax.set_ylabel("kernel value", color=_FG)

        # Bottom row: compact support bump — no clipping
        ax2 = axes[1, idx]
        b = _bump_compact(x, r0, width)
        mass_b = np.trapezoid(b, x)
        ax2.plot(x, b, color=PALETTE["correct"], lw=2.5)
        ax2.fill_between(x, 0, b, color=PALETTE["correct"], alpha=0.15)
        ax2.axvline(0, color=PALETTE["muted"], lw=0.8, ls=":", alpha=0.6)
        ax2.axvline(1, color=PALETTE["muted"], lw=0.8, ls=":", alpha=0.6)
        ax2.set_title(f"Compact support, {lab}\n(mass = {mass_b:.2f})", fontsize=11)
        ax2.set_xlabel(r"$r$")
        ax2.set_xlim(-0.05, 1.05)
        if idx == 0:
            ax2.set_ylabel("kernel value", color=_FG)

    fig.tight_layout()
    save(fig, "fig_compact_vs_gaussian", ps.output_dir())
    print("wrote fig_compact_vs_gaussian")


if __name__ == "__main__":
    main()
