"""FC6-1: per-step contraction factors and their cost, GD vs CG.

Left: the contraction factors (kappa-1)/(kappa+1) and
(sqrt(kappa)-1)/(sqrt(kappa)+1) as functions of kappa.
Right: iterations needed to shrink the energy error by 10^6.
"""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import HALO, GROUND

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

kappa = np.geomspace(1.0001, 1e4, 400)
rho_gd = (kappa - 1) / (kappa + 1)
rho_cg = (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)

fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.5, 4.8))

axl.semilogx(kappa, rho_gd, color=PALETTE["naive"], lw=2.4,
             label=r"gradient descent: $\dfrac{\kappa-1}{\kappa+1}$")
axl.semilogx(kappa, rho_cg, color=PALETTE["correct"], lw=2.4,
             label=r"conjugate gradients: $\dfrac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}$")
axl.set_xlabel(r"condition number $\kappa$")
axl.set_ylabel("error factor per step")
axl.set_ylim(0, 1.02)
axl.set_title("how much survives each step")
axl.legend(loc="lower right", fontsize=11, frameon=True,
           facecolor=GROUND, edgecolor="none", framealpha=0.9)

iters_gd = np.log(1e-6) / np.log(rho_gd)
iters_cg = np.log(1e-6) / np.log(rho_cg)
axr.loglog(kappa, iters_gd, color=PALETTE["naive"], lw=2.4, label="gradient descent")
axr.loglog(kappa, iters_cg, color=PALETTE["correct"], lw=2.4, label="conjugate gradients")
axr.set_xlabel(r"condition number $\kappa$")
axr.set_ylabel(r"steps to reduce the error $10^6\times$")
axr.set_title(r"$\kappa$ vs $\sqrt{\kappa}$, in iterations")
axr.legend(loc="upper left", fontsize=11, frameon=True,
           facecolor=GROUND, edgecolor="none", framealpha=0.9)

k0 = 1e4
axr.annotate(f"$\\kappa = 10^4$:\n{iters_gd[-1]:,.0f} steps",
             xy=(0.75 * k0, np.interp(0.75 * k0, kappa, iters_gd)), xytext=(4e2, 2.2e4),
             color=PALETTE["naive"], fontsize=10.5, ha="center", bbox=HALO,
             arrowprops=dict(arrowstyle="->", color=PALETTE["naive"], lw=1.0,
                             connectionstyle="arc3,rad=-0.15"))
axr.annotate(f"{iters_cg[-1]:,.0f} steps",
             xy=(0.8 * k0, np.interp(0.8 * k0, kappa, iters_cg)), xytext=(3.5e3, 3.2e1),
             color=PALETTE["correct"], fontsize=10.5, ha="center", bbox=HALO,
             arrowprops=dict(arrowstyle="->", color=PALETTE["correct"], lw=1.0,
                             connectionstyle="arc3,rad=0.15"))

fig.tight_layout()
save(fig, "fig_cg6_rates", OUT)
