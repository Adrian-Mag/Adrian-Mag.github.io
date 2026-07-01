"""Figure: A single target kernel T(r) as a smooth bump with unit area.

Used in Act 1 (The Kernel Game). Shows one localised target kernel
centred at r=0.5, with the model m(r) shown faintly in the background.
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
    model_space = ps.make_model_space()
    target = ps.make_target(model_space)
    m_bar = ps.true_model(model_space)
    x = ps.plot_grid()

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Target kernel — prominent, on the left y-axis
    k_mid = ps.N_P // 2
    tk = target.get_kernel(k_mid)
    ax.plot(x, tk.evaluate(x), color=PALETTE["correct"], lw=2.8,
            label=r"target kernel $\mathcal{T}_k(r)$")
    ax.fill_between(x, 0, tk.evaluate(x), color=PALETTE["correct"], alpha=0.15)
    ax.set_ylabel("kernel value", color=PALETTE["correct"])
    ax.tick_params(axis="y", labelcolor=PALETTE["correct"])

    # Model — on a twin axis so it is visible despite different magnitude
    ax2 = ax.twinx()
    ax2.plot(x, m_bar.evaluate(x), color=PALETTE["true"], alpha=0.7, lw=1.8,
             label=r"model $m(r)$")
    ax2.fill_between(x, 0, m_bar.evaluate(x), color=PALETTE["true"], alpha=0.08)
    ax2.set_ylabel("model value", color=PALETTE["true"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["true"])

    ax.set_title(r"A target kernel: the desired question")
    ax.set_xlabel(r"$r$")
    ax.set_xlim(0, 1)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    fig.tight_layout()
    save(fig, "fig_target_kernel", ps.output_dir())
    print("wrote fig_target_kernel")


if __name__ == "__main__":
    main()
