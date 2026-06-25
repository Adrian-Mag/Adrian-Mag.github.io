"""Figure F3 - L^2 elements are equivalence classes; point evaluation is meaningless.

Show two functions that differ on a set of measure zero (e.g. at a single point
and on a fat Cantor set) but are the same element of L^2. Visually, they look
identical almost everywhere, illustrating that "the value at z=0.5" is not a
well-defined question for an L^2 function.
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
    x = ps.plot_grid()
    m_bar = ps.true_model(ps.make_model_space())
    y = np.asarray(m_bar.evaluate(x), dtype=float)

    # Variant 1: same function, but with a spike at one point (measure zero)
    y_spike = y.copy()
    idx_spike = np.argmin(np.abs(x - 0.5))
    y_spike[idx_spike] += 5.0

    # Variant 2: same function, but modified on a "fat Cantor set" (positive measure
    # but empty interior). We approximate by adding a bump on a small interval
    # and removing it — to show that functions differing on sets of measure zero
    # are the same in L^2, while functions differing on positive measure are not.
    # For the figure, we show three curves:
    #   (a) the "true" function m
    #   (b) m + spike at a point  — same L^2 element
    #   (c) m + perturbation on a set of positive measure — different L^2 element

    y_perturbed = y.copy()
    mask = (x > 0.3) & (x < 0.35)
    y_perturbed[mask] += 1.5

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: point spike — same element of L^2
    ax = axes[0]
    ax.plot(x, y, color=PALETTE["true"], lw=2.5, label=r"$m(z)$")
    ax.plot(x, y_spike, color=PALETTE["naive"], lw=1.5, ls="--",
            label=r"$\tilde{m}(z)$: differs at one point")
    ax.set_title(r"Same element of $L^2$: differ on a null set")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend(fontsize=9)

    # Right panel: perturbation on positive measure — different element
    ax = axes[1]
    ax.plot(x, y, color=PALETTE["true"], lw=2.5, label=r"$m(z)$")
    ax.plot(x, y_perturbed, color=PALETTE["correct"], lw=1.5, ls="--",
            label=r"$\tilde{m}(z)$: differs on positive measure")
    ax.set_title(r"Different elements of $L^2$: differ on positive measure")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend(fontsize=9)

    fig.tight_layout()
    save(fig, "fig3_l2_equivalence_classes", ps.output_dir())
    print("wrote fig3_l2_equivalence_classes")


if __name__ == "__main__":
    main()
