"""FC3-1: the same descent seen in the two geometries.

Left: original coordinates — elliptical contours, zigzag path.
Right: coordinates stretched by A^(1/2) — the landscape becomes perfectly
round, and the mapped path visibly keeps aiming at the wrong point.
"""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import make_A, J, gd_path, contour_levels, worst_start, HALO

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

A = make_A(8.0)
x0 = worst_start(A, scale=2.3, signs=(-1.0, 1.0))
if x0[0] > 0:
    x0 = -x0
xs = gd_path(A, x0, tol=0.0, maxit=12)

# A^(1/2) via the eigendecomposition
w, V = np.linalg.eigh(A)
S = V @ np.diag(np.sqrt(w)) @ V.T
ws = xs @ S.T

fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.5, 5.2))

# --- left: the landscape as drawn -------------------------------------------
lim = 2.7
g = np.linspace(-lim, lim, 260)
X, Y = np.meshgrid(g, g)
axl.contour(X, Y, J(A, X, Y), levels=contour_levels(A, [xs], n=8),
            cmap=PALETTE["mako"], linewidths=1.2, alpha=0.75)
axl.plot(xs[:, 0], xs[:, 1], "-o", color=PALETTE["true"], lw=2.0, markersize=3.2)
axl.plot(0, 0, marker="*", color=PALETTE["correct"], markersize=14, zorder=6)
axl.set_title("the landscape as we drew it")
axl.set_xlabel(r"$v_1$")
axl.set_ylabel(r"$v_2$")
axl.set_xlim(-lim, lim)
axl.set_ylim(-2.6, 2.3)
axl.set_aspect("equal")

# --- right: the landscape as A measures it ----------------------------------
wmax = np.abs(ws).max() * 1.18
gw = np.linspace(-wmax, wmax, 260)
XW, YW = np.meshgrid(gw, gw)
ZW = 0.5 * (XW ** 2 + YW ** 2)
axr.contour(XW, YW, ZW, levels=contour_levels(A, [xs], n=8),
            cmap=PALETTE["mako"], linewidths=1.2, alpha=0.75)
axr.plot(ws[:, 0], ws[:, 1], "-o", color=PALETTE["true"], lw=2.0, markersize=3.2)
axr.plot(0, 0, marker="*", color=PALETTE["correct"], markersize=14, zorder=6)

# the direction the method SHOULD take from the start, in this geometry
p0 = ws[0]
axr.annotate("", xy=(0.03 * p0[0], 0.03 * p0[1]), xytext=(p0[0], p0[1]),
             arrowprops=dict(arrowstyle="-|>", color=PALETTE["correct"], lw=2.2,
                             ls="--", mutation_scale=16))
axr.annotate("in a round bowl, downhill\npoints straight at the answer",
             xy=(0.5 * p0[0], 0.5 * p0[1]), xytext=(0.06 * wmax, 0.62 * wmax),
             color=PALETTE["correct"], fontsize=11, bbox=HALO,
             arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.1))
axr.annotate("but the mapped path shows the\nmethod aiming somewhere else",
             xy=(ws[1, 0], ws[1, 1]), xytext=(-0.98 * wmax, -0.8 * wmax),
             color=FG, fontsize=11, bbox=HALO,
             arrowprops=dict(arrowstyle="->", color=FG, lw=1.1))

axr.set_title("the landscape as $A$ measures it  ($w = A^{1/2}v$)")
axr.set_xlabel(r"$w_1$")
axr.set_ylabel(r"$w_2$")
axr.set_xlim(-wmax, wmax)
axr.set_ylim(-wmax, wmax)
axr.set_aspect("equal")

fig.tight_layout()
save(fig, "fig_cg3_stretch", OUT)
