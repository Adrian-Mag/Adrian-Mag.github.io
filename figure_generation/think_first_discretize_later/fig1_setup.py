"""Figure F1 - the problem setup.

Three panels: (a) the sensitivity kernels of the forward operator, (b) the true
model, and (c) the noise-free vs noisy data. Establishes that the model is a
function and the data are a handful of weighted integrals.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    x = ps.plot_grid()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

    # (a) Sensitivity kernels — mako gradient across kernels
    ax = axes[0]
    colors = mako_light_n(ps.N_D)
    for i in range(ps.N_D):
        ax.plot(x, forward.get_kernel(i).evaluate(x), color=colors[i],
                alpha=0.8, lw=1.6)
    ax.set_title(r"(a) Sensitivity kernels $K_i(z)$")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("kernel value")

    # (b) True model — amber for the truth
    ax = axes[1]
    ax.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.6)
    ax.set_title(r"(b) True model $\bar{m}(z)$")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")

    # (c) Data: noise-free vs noisy
    ax = axes[2]
    idx = np.arange(ps.N_D)
    for i in idx:
        ax.plot([i, i], [data.d_clean[i], data.d[i]], color=PALETTE["muted"],
                alpha=0.5, lw=1.0)
    ax.scatter(idx, data.d_clean, color=PALETTE["true"], marker="x", s=70,
               lw=2.5, label=r"noise-free $\bar{\mathbf{d}}=G\bar{m}$", zorder=5)
    ax.errorbar(idx, data.d, yerr=data.noise_std, fmt="o", color=PALETTE["data"],
                ms=7, capsize=3, label=r"noisy data $\tilde{\mathbf{d}}$", zorder=4)
    ax.set_title(r"(c) Data: a few noisy integrals")
    ax.set_xlabel(r"observation index $i$")
    ax.set_ylabel(r"$[\tilde{\mathbf{d}}]_i$")
    ax.legend()

    fig.tight_layout()
    save(fig, "fig1_setup", ps.output_dir())
    print("wrote fig1_setup")


if __name__ == "__main__":
    main()
