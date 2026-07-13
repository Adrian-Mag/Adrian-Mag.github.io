"""FC4-1: conjugate directions finish a 2-D problem in two steps,
starting along ANY first direction — with the steepest-descent zigzag
shown as a ghost for contrast."""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import make_A, J, gd_path, conjugate_path, contour_levels, worst_start, HALO

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

A = make_A(8.0)
x0 = worst_start(A, scale=2.3, signs=(-1.0, 1.0))
if x0[0] > 0:
    x0 = -x0

# a deliberately generic first direction (NOT the residual)
ang = np.deg2rad(-18.0)
p0 = np.array([np.cos(ang), np.sin(ang)])
cj = conjugate_path(A, x0, p0)
gd = gd_path(A, x0, tol=1e-9)

lim = 2.7
g = np.linspace(-lim, lim, 260)
X, Y = np.meshgrid(g, g)

fig, ax = plt.subplots(figsize=(9.2, 5.6))
ax.contour(X, Y, J(A, X, Y), levels=contour_levels(A, [gd, cj], n=8),
           cmap=PALETTE["mako"], linewidths=1.2, alpha=0.7)

ax.plot(gd[:, 0], gd[:, 1], "-o", color=PALETTE["muted"], lw=1.4,
        markersize=2.6, alpha=0.85, zorder=4,
        label=f"steepest descent ({len(gd) - 1} steps)")
ax.plot(cj[:, 0], cj[:, 1], "-o", color=PALETTE["correct"], lw=2.6,
        markersize=5.5, zorder=6, label="conjugate directions (2 steps)")
ax.plot(0, 0, marker="*", color=PALETTE["true"], markersize=16, zorder=7)

ax.annotate("$u_0$", xy=(cj[0, 0], cj[0, 1]), xytext=(cj[0, 0] + 0.14, cj[0, 1] - 0.1),
            color=FG, fontsize=12, bbox=HALO)
ax.annotate("$u_1$: line search along a first\ndirection $p_0$ we chose freely",
            xy=(cj[1, 0], cj[1, 1]), xytext=(-2.55, -1.05),
            color=FG, fontsize=11, bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=FG, lw=1.1))
ax.annotate("$u_2 = u$: the second direction is forced —\nit must be $A$-perpendicular to $p_0$,"
            "\nand it lands exactly on the solution",
            xy=(0.06, -0.06), xytext=(0.42, -1.6), color=PALETTE["correct"], fontsize=11, bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.1))

ax.set_xlim(-lim, lim)
ax.set_ylim(-2.6, 2.3)
ax.set_aspect("equal")
ax.set_xlabel(r"$v_1$")
ax.set_ylabel(r"$v_2$")
ax.set_title(r"same landscape ($\kappa = 8$), no zigzag: $(Ap_0, p_1) = 0$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)

fig.tight_layout()
save(fig, "fig_cg4_twostep", OUT)
