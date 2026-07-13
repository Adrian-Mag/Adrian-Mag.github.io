"""FC2-1: exact line search — J restricted to a ray is a parabola in alpha."""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import make_A, J, HALO

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

A = make_A(8.0)
x0 = np.array([-2.0, 1.5])
r = -(A @ x0)
rr = r @ r
rAr = r @ (A @ r)
J0 = J(A, x0[0], x0[1])
a_star = rr / rAr

alphas = np.linspace(-0.25 * a_star, 2.35 * a_star, 300)
phi = J0 - alphas * rr + 0.5 * alphas ** 2 * rAr
phi_min = J0 - a_star * rr + 0.5 * a_star ** 2 * rAr

fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.plot(alphas, phi, color=PALETTE["mako_dark"], lw=2.6)
ax.axvline(a_star, color=PALETTE["muted"], lw=1.2, ls="--")
ax.plot([a_star], [phi_min], "o", color=PALETTE["true"], markersize=9, zorder=5)
ax.plot([0], [J0], "o", color=PALETTE["correct"], markersize=7, zorder=5)

ax.annotate(r"start: $\alpha = 0$, height $J(u_k)$",
            xy=(0, J0), xytext=(0.18 * a_star, J0 + 2.5),
            color=PALETTE["correct"], fontsize=11, bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.1))
ax.annotate("the parabola bottoms out here:\n"
            r"$\varphi'(\alpha_k)=0 \ \Leftrightarrow\ \alpha_k = \dfrac{(r_k, r_k)}{(Ar_k, r_k)}$",
            xy=(a_star, phi_min + 1.2), xytext=(a_star, 0.62 * J0),
            color=FG, fontsize=11.5, ha="center", va="center", bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=FG, lw=1.1))
ax.annotate("too far: $J$ rises again", xy=(2.05 * a_star, np.interp(2.05 * a_star, alphas, phi)),
            xytext=(1.35 * a_star, J0 + 2.7), color=PALETTE["muted"], fontsize=10.5, bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.0))

ax.set_xlabel(r"step length $\alpha$")
ax.set_ylabel(r"$\varphi(\alpha) = J(u_k + \alpha\, r_k)$")
ax.set_title("along a fixed direction, $J$ is just a parabola")

fig.tight_layout()
save(fig, "fig_cg2_linesearch", OUT)
