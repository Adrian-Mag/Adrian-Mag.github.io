"""FC2-2: the steepest-descent zigzag on an ill-conditioned landscape."""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import make_A, J, gd_path, energy_norm, contour_levels, worst_start, HALO, GROUND

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

N_SHOW = 20
A = make_A(20.0)
x0 = worst_start(A, scale=2.4, signs=(-1.0, 1.0))
if x0[0] > 0:
    x0 = -x0
xs = gd_path(A, x0, tol=0.0, maxit=N_SHOW)

lim = 2.6
g = np.linspace(-lim, lim, 260)
X, Y = np.meshgrid(g, g)
Z = J(A, X, Y)

fig, ax = plt.subplots(figsize=(9.2, 5.6))
ax.contour(X, Y, Z, levels=contour_levels(A, [xs], n=9),
           cmap=PALETTE["mako"], linewidths=1.2, alpha=0.75)
ax.plot(xs[:, 0], xs[:, 1], "-o", color=PALETTE["true"], lw=2.0,
        markersize=3.4, zorder=5)
ax.plot(0, 0, marker="*", color=PALETTE["correct"], markersize=15, zorder=6)
ax.plot(xs[0, 0], xs[0, 1], "o", color=PALETTE["naive"], markersize=8, zorder=6)

ax.annotate("start $u_0$", xy=(xs[0, 0], xs[0, 1]), xytext=(xs[0, 0] + 0.35, xs[0, 1] - 0.12),
            color=PALETTE["naive"], fontsize=11.5, ha="left", bbox=HALO)
ax.annotate("the solution", xy=(0.08, -0.05), xytext=(0.85, -0.85), color=PALETTE["correct"],
            fontsize=11.5, bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.1))
corner = xs[1]
ax.annotate("every turn is a perfect\nright angle (Euclidean)",
            xy=(corner[0] - 0.05, corner[1] - 0.02), xytext=(-2.52, -1.15),
            color=FG, fontsize=11.5, ha="left", bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=FG, lw=1.1,
                            connectionstyle="arc3,rad=0.15"))

# inset: energy error per iteration
err = np.array([energy_norm(A, x) for x in xs])
axin = ax.inset_axes([0.66, 0.66, 0.31, 0.30])
axin.patch.set_facecolor(GROUND)
axin.patch.set_alpha(0.92)
axin.semilogy(np.arange(len(err)), err / err[0], color=PALETTE["naive"], lw=2.0)
axin.set_title(r"energy error $\|u_k - u\|_A$", fontsize=9.5, color=FG).set_bbox(HALO)
axin.tick_params(labelsize=8)
axin.set_xlabel("iteration $k$", fontsize=8.5).set_bbox(HALO)
axin.grid(True, alpha=0.25)

ax.set_xlim(-lim, lim)
ax.set_ylim(-2.65, 2.2)
ax.set_aspect("equal")
ax.set_xlabel(r"$v_1$")
ax.set_ylabel(r"$v_2$")
ax.set_title(rf"steepest descent, $\kappa = 20$: {N_SHOW} steps in, still zigzagging")

fig.tight_layout()
save(fig, "fig_cg2_zigzag", OUT)
