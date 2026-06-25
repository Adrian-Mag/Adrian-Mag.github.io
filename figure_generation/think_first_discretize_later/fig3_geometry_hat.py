"""Figure F4 - naive vs geometry-correct on hats.

Left: on a hat basis the naive (transpose) and geometry-correct
(mass-weighted adjoint) least-norm reconstructions visibly disagree.
Right: the hat Gram (mass) matrix is tridiagonal and non-diagonal.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, plt, save

N_CELLS = 30


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    x = ps.plot_grid()

    disc_hat = ps.discretise(forward, "hat", N_CELLS)
    a_naive = ps.least_norm_coefficients(disc_hat.naive_forward, data)
    a_correct = ps.least_norm_coefficients(disc_hat.correct_forward, data)
    f_naive = ps.reconstruct(disc_hat.function_space, a_naive)
    f_correct = ps.reconstruct(disc_hat.function_space, a_correct)
    max_diff = float(np.max(np.abs(a_naive - a_correct)))

    fig = plt.figure(figsize=(14, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0])

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.plot(x, m_bar.evaluate(x), color=PALETTE["true"], lw=2.4, label="true model")
    ax0.plot(x, f_naive.evaluate(x), color=PALETTE["naive"], lw=2.2, ls="--",
             label=r"naive  ($G^{\top}$)")
    ax0.plot(x, f_correct.evaluate(x), color=PALETTE["correct"], lw=2.2,
             label=r"correct  ($M^{-1}G^{\top}$)")
    ax0.set_title(rf"Hat basis: naive vs correct  (max$|\Delta\alpha|$ = {max_diff:.2f})")
    ax0.set_xlabel(r"depth $z$")
    ax0.set_ylabel("model value")
    ax0.legend()

    ax_h = fig.add_subplot(gs[0, 1])
    im = ax_h.imshow(disc_hat.gram, cmap="cividis")
    ax_h.set_title(r"hat Gram $M$  (tridiagonal)")
    ax_h.set_xticks([])
    ax_h.set_yticks([])
    ax_h.grid(False)
    fig.colorbar(im, ax=ax_h, fraction=0.046, pad=0.04)

    fig.tight_layout()
    save(fig, "fig3b_geometry_hat", ps.output_dir())
    print(f"wrote fig3b_geometry_hat (max|dalpha|={max_diff:.3f})")


if __name__ == "__main__":
    main()
