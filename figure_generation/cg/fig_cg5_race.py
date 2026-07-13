"""FC5-1: gradient descent vs conjugate gradients on a 200-dimensional
problem, at two condition numbers. Energy-norm error per iteration."""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import HALO

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

rng = np.random.default_rng(7)
N = 200
ITERS = 60


def run(kappa):
    """Return per-iteration relative energy errors for GD and CG."""
    lam = np.geomspace(1.0, kappa, N)
    xstar = rng.standard_normal(N)
    f = lam * xstar

    def energy(x):
        d = x - xstar
        return np.sqrt(np.sum(lam * d * d))

    e0 = energy(np.zeros(N))

    # steepest descent
    x = np.zeros(N)
    gd = [1.0]
    for _ in range(ITERS):
        r = f - lam * x
        a = (r @ r) / (r @ (lam * r))
        x = x + a * r
        gd.append(energy(x) / e0)

    # conjugate gradients
    x = np.zeros(N)
    r = f.copy()
    p = r.copy()
    cg = [1.0]
    for _ in range(ITERS):
        rr = r @ r
        Ap = lam * p
        a = rr / (p @ Ap)
        x = x + a * p
        r = r - a * Ap
        p = r + ((r @ r) / rr) * p
        cg.append(max(energy(x) / e0, 1e-16))

    return np.array(gd), np.array(cg)


fig, ax = plt.subplots(figsize=(9.2, 5.2))
ks = np.arange(ITERS + 1)

for kappa, ls in ((25, "--"), (400, "-")):
    gd, cg = run(kappa)
    ax.semilogy(ks, gd, ls, color=PALETTE["naive"], lw=2.2,
                label=rf"gradient descent, $\kappa={kappa}$")
    ax.semilogy(ks, cg, ls, color=PALETTE["correct"], lw=2.2,
                label=rf"conjugate gradients, $\kappa={kappa}$")

ax.annotate("the $\\sqrt{\\kappa}$ effect, drawn:\nCG at $\\kappa=400$ keeps pace\nwith GD at $\\kappa=25$",
            xy=(48, 1.2e-3), xytext=(51, 1e-6), color=FG, fontsize=11,
            ha="center", bbox=HALO,
            arrowprops=dict(arrowstyle="->", color=FG, lw=1.1,
                            connectionstyle="arc3,rad=-0.15"))

ax.set_ylim(1e-12, 3)
ax.set_xlabel("iteration $k$")
ax.set_ylabel(r"relative energy error $\|u_k - u\|_A \,/\, \|u_0 - u\|_A$")
ax.set_title(r"the same 200-dimensional problem, two methods")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)

fig.tight_layout()
save(fig, "fig_cg5_race", OUT)
