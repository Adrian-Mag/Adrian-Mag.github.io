"""FC1-1: the energy landscape of Au = f.

Left: the quadratic functional J as a bowl-shaped surface.
Right: its contour map, with the residual (= negative gradient) drawn
as the downhill arrow at several points.
"""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import make_A, J, HALO

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

A = make_A(4.0)
lim = 2.5
g = np.linspace(-lim, lim, 220)
X, Y = np.meshgrid(g, g)
Z = J(A, X, Y)

fig = plt.figure(figsize=(11.5, 4.8))

# --- left: the bowl ---------------------------------------------------------
ax3 = fig.add_subplot(1, 2, 1, projection="3d")
ax3.plot_surface(X, Y, Z, cmap=PALETTE["mako"], rstride=4, cstride=4,
                 linewidth=0, antialiased=True, alpha=0.96)
ax3.scatter([0], [0], [0], color=PALETTE["true"], s=45, depthshade=False, zorder=5)
ax3.set_xlabel(r"$v_1$", labelpad=-4)
ax3.set_ylabel(r"$v_2$", labelpad=-4)
ax3.set_zlabel(r"$J(v)$", labelpad=-6)
ax3.set_title("the functional $J$ is a bowl")
ax3.view_init(elev=28, azim=-58)
ax3.set_facecolor("none")
for axis in (ax3.xaxis, ax3.yaxis, ax3.zaxis):
    axis.pane.set_alpha(0.0)
    axis.pane.set_edgecolor((1, 1, 1, 0))
ax3.tick_params(labelsize=9, pad=-2)
ax3.grid(False)

# --- right: contours + downhill arrows --------------------------------------
ax = fig.add_subplot(1, 2, 2)
levels = J(A, lim, 0) * np.power(0.5, np.arange(9))[::-1]
ax.contour(X, Y, Z, levels=levels, cmap=PALETTE["mako"], linewidths=1.4, alpha=0.85)
ax.plot(0, 0, marker="*", color=PALETTE["true"], markersize=15, zorder=6)
ax.annotate("the solution $u$\n(bottom of the bowl)", xy=(0.07, -0.07), xytext=(0.75, -1.95),
            color=FG, fontsize=11, ha="left", bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=FG, lw=1.1))

pts = np.array([[-1.9, 1.4], [1.6, 1.5], [1.9, -0.9], [-1.2, -1.7]])
for p in pts:
    r = -(A @ p)
    r = 0.72 * r / np.linalg.norm(r)
    ax.annotate("", xy=(p[0] + r[0], p[1] + r[1]), xytext=(p[0], p[1]),
                arrowprops=dict(arrowstyle="-|>", color=PALETTE["correct"],
                                lw=2.4, mutation_scale=16))
    ax.plot(p[0], p[1], "o", color=PALETTE["correct"], markersize=4.5)
ax.annotate("the residual $r = f - Av$\npoints downhill", xy=(pts[3, 0] - 0.15, pts[3, 1] - 0.15),
            xytext=(-2.4, -2.05), color=PALETTE["correct"], fontsize=11, ha="left", bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.1))

ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim - 0.3)
ax.set_aspect("equal")
ax.set_xlabel(r"$v_1$")
ax.set_ylabel(r"$v_2$")
ax.set_title("its contour map")

fig.tight_layout()
save(fig, "fig_cg1_landscape", OUT)
