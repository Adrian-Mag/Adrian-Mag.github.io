"""Figure: Visual construction of a resolving kernel as a weighted sum.

Used in Act 2 (Building SOLA from Scratch). Shows a stack of integral
equations, each with a real kernel graph, weights x_i, and a summation
bar, culminating in the resolving kernel integral.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save, FG

_FG = FG


def _plot_kernel_inset(fig, rect, x, yvals, color, lw=1.5, alpha=0.9,
                       fill=True, fill_alpha=0.12):
    """Create a small inset axis showing a kernel curve."""
    ax = fig.add_axes(rect)
    ax.plot(x, yvals, color=color, lw=lw, alpha=alpha)
    if fill:
        ax.fill_between(x, 0, yvals, color=color, alpha=fill_alpha)
    ax.set_xlim(0, 1)
    bottom = min(0, yvals.min() * 1.1)
    top = max(yvals.max() * 1.15, 0.01)
    ax.set_ylim(bottom, top)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax


def main() -> None:
    apply_style()
    prob = ps.make_problem()
    x = prob.x

    k = ps.N_P // 2
    weights = prob.X_noiseless[k, :]
    n_show = min(ps.N_D, 6)
    colors = mako_light_n(ps.N_D)

    # --- Figure layout ---
    n_rows = n_show + 2  # individual rows + bar + combined row
    row_h = 0.9          # inches per row
    fig_w = 9.5
    fig_h = n_rows * row_h + 1.2
    fig = plt.figure(figsize=(fig_w, fig_h))

    # Column positions (figure fraction)
    col_weight = 0.06       # x_i label
    col_integral = 0.12     # integral sign (before kernel)
    col_kernel_l = 0.18     # kernel inset left edge
    col_kernel_r = 0.51     # kernel inset right edge
    kernel_w = col_kernel_r - col_kernel_l
    col_m = 0.63            # m(r) dr
    col_eq = 0.82           # = result

    # Row positions (figure fraction), top to bottom
    top = 0.94
    row_gap = 1.0 / n_rows * 0.85

    row_ys = []
    for i in range(n_show):
        yc = top - i * row_gap - row_gap * 0.5
        row_ys.append(yc)

        ki = prob.forward.get_kernel(i)
        ki_vals = ki.evaluate(x)

        # Weight label
        fig.text(col_weight, yc, fr"$x_{i+1}\cdot$",
                 fontsize=16, ha="center", va="center",
                 color=PALETTE["mako_light"])

        # Kernel inset
        inset_h = 0.055
        rect = [col_kernel_l, yc - inset_h / 2, kernel_w, inset_h]
        _plot_kernel_inset(fig, rect, x, ki_vals, colors[i], lw=1.4)

        # Integral sign
        fig.text(col_integral, yc, r"$\int_\Omega$",
                 fontsize=20, ha="center", va="center",
                 color=PALETTE["muted"])

        # m(r) dr
        fig.text(col_m, yc, r"$m(r)\,\mathrm{d}r$",
                 fontsize=13, ha="center", va="center",
                 color=_FG)

        # = x_i [d]_i
        fig.text(col_eq, yc, fr"$= x_{i+1}\,[\mathbf{{d}}]_{i+1}$",
                 fontsize=13, ha="center", va="center",
                 color=PALETTE["mako_light"])

    # --- Summation bar ---
    bar_y = row_ys[-1] - row_gap * 0.45
    fig.lines.append(
        plt.Line2D([0.05, col_eq + 0.04], [bar_y, bar_y],
                   transform=fig.transFigure,
                   color=PALETTE["muted"], lw=1.8)
    )

    # Plus sign right next to the bar (left side)
    fig.text(0.025, bar_y, r"$+$",
             fontsize=20, ha="center", va="center",
             color=PALETTE["mako_light"])

    # --- Combined resolving kernel row ---
    combined_y = bar_y - row_gap * 1.1

    # Large integral sign
    fig.text(col_integral, combined_y, r"$\int_\Omega$",
             fontsize=26, ha="center", va="center",
             color=PALETTE["muted"])

    # Combined kernel: R(r) = sum x_i K_i
    rk = ps.resolving_kernel(prob.forward, prob.X_noiseless, k, x)

    # Larger inset for the combined kernel
    big_inset_h = 0.09
    rect = [col_kernel_l, combined_y - big_inset_h / 2, kernel_w, big_inset_h]
    ax_r = _plot_kernel_inset(fig, rect, x, rk, PALETTE["mako_dark"],
                               lw=2.5, fill_alpha=0.15)

    # Overlay constituent weighted kernels faintly
    for i in range(n_show):
        ki = prob.forward.get_kernel(i)
        ki_vals = ki.evaluate(x)
        ax_r.plot(x, ki_vals * weights[i], color=colors[i], alpha=0.2, lw=0.7)

    # Horizontal brace under the combined kernel inset, with R(r) label below
    brace_y = combined_y - big_inset_h / 2 - 0.018
    brace_left = col_kernel_l
    brace_right = col_kernel_r
    brace_mid = (brace_left + brace_right) / 2
    brace_dip = 0.025
    # Draw brace as a single polyline: left vertical up, diagonal down to center, diagonal up to right, right vertical up
    fig.lines.append(plt.Line2D(
        [brace_left, brace_left, brace_mid - 0.008, brace_mid + 0.008, brace_right, brace_right],
        [brace_y + brace_dip * 0.4, brace_y, brace_y - brace_dip, brace_y - brace_dip, brace_y, brace_y + brace_dip * 0.4],
        transform=fig.transFigure, color=PALETTE["mako_dark"], lw=1.8))

    # R(r) label below the brace
    fig.text(brace_mid, brace_y - brace_dip - 0.008,
             r"$R(r)$", fontsize=16, ha="center", va="top",
             color=PALETTE["mako_dark"])

    # m(r) dr
    fig.text(col_m, combined_y, r"$m(r)\,\mathrm{d}r$",
             fontsize=13, ha="center", va="center",
             color=_FG)

    # = sum x_i [d]_i
    fig.text(col_eq, combined_y, r"$= \sum_i x_i\,[\mathbf{d}]_i$",
             fontsize=14, ha="center", va="center",
             color=PALETTE["mako_light"])

    # Title
    fig.text(0.5, 0.985, r"Building a resolving kernel from weighted data",
             fontsize=16, ha="center", va="top",
             color=_FG, fontweight="bold")

    save(fig, "fig_resolving_kernel_construction", ps.output_dir())
    print("wrote fig_resolving_kernel_construction")


if __name__ == "__main__":
    main()
