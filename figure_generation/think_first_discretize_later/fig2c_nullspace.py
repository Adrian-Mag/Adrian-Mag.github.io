"""Figure F2c - null space of G: invisible coefficient directions.

Two panels: (a) null-space coefficient vectors as an imshow heatmap (rows =
null-space basis vectors, columns = coefficient indices — coefficient world),
and (b) the corresponding function reconstructions (function world). These
functions are invisible to the data: adding any of them to a model does not
change the predicted data.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps
from style import PALETTE, apply_style, mako_light_n, plt, save, FG

N_CELLS = 30
N_SHOW = 4  # number of null-space vectors to display


def main() -> None:
    apply_style()
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    m_bar = ps.true_model(model_space)
    data = ps.make_data(forward, m_bar)
    x = ps.plot_grid()

    box = ps.hat_coeff_space(N_CELLS)
    fs = box.function_space

    # Get the forward matrix G
    disc = ps.discretise(forward, "hat", N_CELLS)
    g_mat = disc.forward_matrix  # shape (K, N)

    # Null space via SVD
    u_svd, s, vh = np.linalg.svd(g_mat)
    rank = np.sum(s > 1e-10)
    null_basis = vh[rank:]  # shape (N-rank, N)

    # Pick a few null-space vectors and scale them for visibility
    null_vecs = null_basis[:N_SHOW]
    # Scale so reconstructions have comparable amplitude to the true model
    scales = []
    for v in null_vecs:
        v_func = np.asarray(fs.from_components(v).evaluate(x), dtype=float)
        peak = np.max(np.abs(v_func))
        scales.append(1.0 / peak if peak > 0 else 1.0)
    null_vecs_scaled = null_vecs * np.array(scales)[:, None]

    # Reconstruct functions from null-space coefficients
    null_funcs = np.asarray(
        [np.asarray(fs.from_components(v).evaluate(x), dtype=float)
         for v in null_vecs_scaled],
        dtype=float,
    )

    # Verify: G @ v = 0 for each null vector
    checks = [np.max(np.abs(g_mat @ v)) for v in null_vecs_scaled]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1.0, 1.3]})

    # (a) Null-space coefficients as imshow — coefficient world
    ax = axes[0]
    im = ax.imshow(null_vecs_scaled, aspect="auto", cmap=PALETTE["mako"],
                   origin="upper", interpolation="nearest")
    ax.set_title(rf"(a) Null-space coefficients $\mathbf{{v}}_k \in \mathcal{{N}}(\mathbf{{G}})$ ($N={N_CELLS}$)")
    ax.set_xlabel(r"coefficient index $j$")
    ax.set_ylabel(r"null-space vector $k$")
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("coefficient value", color=PALETTE.get("muted", FG))
    cbar.ax.tick_params(colors=PALETTE.get("muted", FG))

    # (b) Function reconstructions — function world
    ax = axes[1]
    colors = mako_light_n(N_SHOW)
    for k in range(N_SHOW):
        ax.plot(x, null_funcs[k], color=colors[k], alpha=0.7, lw=1.8,
                label=rf"$\mathbf{{v}}_{{{k+1}}}$: $\mathbf{{G}}\mathbf{{v}}={checks[k]:.1e}$")
    ax.axhline(0, color=PALETTE["muted"], lw=1.0, linestyle="--", alpha=0.5)
    ax.set_title(r"(b) Functions invisible to the data")
    ax.set_xlabel(r"depth $z$")
    ax.set_ylabel("model value")
    ax.legend(fontsize=10)

    fig.tight_layout()
    save(fig, "fig2c_nullspace", ps.output_dir())
    print(f"wrote fig2c_nullspace (rank={rank}, null dim={N_CELLS - rank})")


if __name__ == "__main__":
    main()
