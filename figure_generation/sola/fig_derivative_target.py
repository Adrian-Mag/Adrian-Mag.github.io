"""Figure: A bump target kernel and its derivative as a contrast target.

Used in Act 4 (Beyond Averages). Shows a localised averaging bump T_k(r)
and its derivative T_k'(r) — a positive/negative lobe kernel that detects
change rather than level.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save


def _bump(r, r0, width):
    """Unit-area Gaussian bump centred at r0."""
    g = np.exp(-((r - r0) / width) ** 2)
    g /= np.trapezoid(g, r)
    return g


def main() -> None:
    apply_style()
    x = ps.plot_grid()

    r0 = 0.5
    width = 0.06

    bump = _bump(x, r0, width)
    # Numerical derivative of the normalised bump
    dbump = np.gradient(bump, x)
    # Normalise so the positive lobe has unit height (for visual clarity)
    dbump /= np.max(np.abs(dbump))

    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(x, bump, color=PALETTE["correct"], lw=2.8,
            label=r"averaging target $T_k(r)$")
    ax.fill_between(x, 0, bump, color=PALETTE["correct"], alpha=0.12)

    ax.plot(x, dbump, color=PALETTE["naive"], lw=2.8,
            label=r"derivative target $T_k'(r)$")
    ax.fill_between(x, 0, dbump, color=PALETTE["naive"], alpha=0.10)

    ax.axhline(0, color=PALETTE["muted"], lw=0.8, ls="-", alpha=0.5)
    ax.set_xlabel(r"$r$")
    ax.set_ylabel("kernel value")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper right")

    fig.tight_layout()
    save(fig, "fig_derivative_target", ps.output_dir())
    print("wrote fig_derivative_target")


if __name__ == "__main__":
    main()
