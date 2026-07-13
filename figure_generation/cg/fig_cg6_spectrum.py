"""FC6-2: CG sees the whole spectrum, not just its endpoints.

Two 60-dimensional problems with the SAME condition number (kappa = 90):
one with eigenvalues in three tight clusters, one with eigenvalues spread
evenly (geometrically). Same kappa, very different CG behaviour.
"""

from pathlib import Path

import numpy as np

from style import PALETTE, FG, apply_style, save, plt
from quad import GROUND

OUT = Path(__file__).resolve().parents[2] / "media" / "research" / "cg"

apply_style()

rng = np.random.default_rng(3)
N = 60
ITERS = 35

# the limiting case of tight clustering: three exactly repeated eigenvalues
lam_clustered = np.repeat([1.0, 11.0, 90.0], N // 3)
lam_spread = np.geomspace(1.0, 90.0, N)


def cg_errors(lam):
    xstar = rng.standard_normal(N)
    f = lam * xstar

    def energy(x):
        d = x - xstar
        return np.sqrt(np.sum(lam * d * d))

    e0 = energy(np.zeros(N))
    x = np.zeros(N)
    r = f.copy()
    p = r.copy()
    errs = [1.0]
    for _ in range(ITERS):
        rr = r @ r
        if rr < 1e-28:
            break
        Ap = lam * p
        a = rr / (p @ Ap)
        x = x + a * p
        r = r - a * Ap
        p = r + ((r @ r) / rr) * p
        errs.append(max(energy(x) / e0, 1e-16))
    return np.array(errs)


fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.5, 4.8),
                               gridspec_kw={"width_ratios": [1, 1.35]})

# --- left: the two spectra ---------------------------------------------------
axl.eventplot([lam_clustered], lineoffsets=1.0, linelengths=0.45,
              colors=[PALETTE["correct"]], linewidths=1.4)
axl.eventplot([lam_spread], lineoffsets=0.0, linelengths=0.45,
              colors=[PALETTE["true"]], linewidths=1.4)
axl.set_xscale("log")
axl.set_yticks([1.0, 0.0])
axl.set_yticklabels(["three clusters", "spread out"])
axl.set_xlabel(r"eigenvalues of $A$ (log scale)")
axl.set_title(r"two spectra, same $\kappa = 90$")
axl.set_ylim(-0.6, 1.6)

# --- right: CG on both -------------------------------------------------------
e_cl = cg_errors(lam_clustered)
e_sp = cg_errors(lam_spread)
axr.semilogy(np.arange(len(e_cl)), e_cl, "-o", color=PALETTE["correct"],
             lw=2.2, markersize=4.2, label="clustered spectrum")
axr.semilogy(np.arange(len(e_sp)), e_sp, "-o", color=PALETTE["true"],
             lw=2.2, markersize=3.4, label="spread-out spectrum")
axr.set_ylim(1e-14, 3)
axr.set_xlabel("iteration $k$")
axr.set_ylabel("relative energy error")
axr.set_title("CG solves one cluster per step, roughly")
axr.legend(loc="upper right", fontsize=11, frameon=True,
           facecolor=GROUND, edgecolor="none", framealpha=0.9)

fig.tight_layout()
save(fig, "fig_cg6_spectrum", OUT)
