"""Figure F5 - boundary conditions as prior beliefs.

A prior covariance in function space is an operator, and it needs boundary
conditions. Two panels show posterior-consistent prior sample realisations from
a smoothing covariance under Neumann (top) and Dirichlet-Neumann (bottom)
boundary conditions, with the zero mean drawn for reference. Mirrors the EGU
poster's boundary-condition panel.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import problem_setup as ps
from style import PALETTE, apply_style, plt, save

N_SAMPLES = 5


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    x = ps.plot_grid()

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    panels = [("neumann", "Neumann"), ("mixed_dn", "Dirichlet-Neumann")]
    for ax, (bc_name, title) in zip(axes, panels):
        covariance = ps.proper_covariance(model_space, bc_name)
        samples = ps.prior_samples(covariance, n_samples=N_SAMPLES, seed=3)
        for sample in samples:
            ax.plot(x, sample.evaluate(x), color=PALETTE["accent"], alpha=0.7, lw=1.6)
        ax.axhline(0.0, color=PALETTE["muted"], lw=1.6, ls="--", label="zero mean")
        ax.set_title(f"{title} prior: sample realisations")
        ax.set_ylabel("model value")
        ax.legend(loc="upper right")
    axes[-1].set_xlabel(r"depth $z$")

    fig.tight_layout()
    save(fig, "fig5_boundary_conditions", ps.output_dir())
    print("wrote fig5_boundary_conditions")


if __name__ == "__main__":
    main()
