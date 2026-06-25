"""Figure F6f - Laplacian covariance as a smoothing prior.

Pre-computes KL expansion samples using intervalinf's BesselSobolevInverse
for combinations of alpha, kappa, s, and boundary conditions.  Saves each
as a transparent PNG.

Output: media/research/think-first/f6f_{alpha}_{kappa}_{s}_{bc}.png
"""

from __future__ import annotations

import os
import sys
import itertools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

from intervalinf import IntervalDomain, Lebesgue
from intervalinf.operators import BesselSobolevInverse, Laplacian
from intervalinf.core.boundary import BoundaryConditions
from intervalinf.sampling import KLSampler

from style import PALETTE, apply_style, mako_light_n, plt, save
from problem_setup import output_dir, DOMAIN

ALPHA_VALUES = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
KAPPA_VALUES = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
S_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
BC_VALUES = ["dirichlet", "neumann", "mixed"]

N_SAMPLES = 3
N_MODES = 80
N_GRID = 500
SEED = 42

BC_FACTORIES = {
    "dirichlet": BoundaryConditions.dirichlet,
    "neumann": BoundaryConditions.neumann,
    "mixed": BoundaryConditions.mixed_dirichlet_neumann,
}


def _make_covariance(alpha, kappa, s, bc_name, M):
    bc = BC_FACTORIES[bc_name]()
    length = DOMAIN[1] - DOMAIN[0]
    lap = Laplacian(M, bc, length, method="spectral", dofs=120)
    return BesselSobolevInverse(
        M, M, kappa, s, lap,
        dofs=120, n_samples=N_SAMPLES, use_fast_transforms=True,
    )


def _samples_for_params(alpha, kappa, s, bc_name, M, x):
    cov = _make_covariance(alpha, kappa, s, bc_name, M)
    sampler = KLSampler(cov, n_modes=N_MODES, rng=np.random.default_rng(SEED))
    samples = sampler.samples(N_SAMPLES)
    arr = np.asarray(
        [np.asarray(f.evaluate(x), dtype=float) for f in samples],
        dtype=float,
    )
    return arr * np.sqrt(alpha)


def _save_panel_png(samples, x, bc_name, out_path):
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    colors = mako_light_n(N_SAMPLES)
    for k in range(samples.shape[0]):
        ax.plot(x, samples[k], color=colors[k], lw=1.5, alpha=0.7)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel(r"$m(x)$", fontsize=10)
    ax.tick_params(labelsize=8)
    bc_label = bc_name.capitalize()
    ax.text(0.98, 0.95, bc_label, transform=ax.transAxes,
            ha="right", va="top", fontsize=8, color=PALETTE["correct"],
            alpha=0.6)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight", transparent=True)
    plt.close(fig)


def main() -> None:
    apply_style()

    domain = IntervalDomain(*DOMAIN)
    M = Lebesgue(0, domain, basis=None)
    x = np.linspace(DOMAIN[0], DOMAIN[1], N_GRID)

    out_dir = output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    total = len(ALPHA_VALUES) * len(KAPPA_VALUES) * len(S_VALUES) * len(BC_VALUES)

    for alpha, kappa, s, bc_name in itertools.product(
        ALPHA_VALUES, KAPPA_VALUES, S_VALUES, BC_VALUES
    ):
        count += 1
        key = f"{alpha:.1f}_{kappa:.1f}_{s:.1f}_{bc_name}"
        fname = out_dir / f"f6f_{key}.png"

        try:
            samples = _samples_for_params(alpha, kappa, s, bc_name, M, x)
            _save_panel_png(samples, x, bc_name, fname)
            if count % 100 == 0 or count == total:
                print(f"  [{count}/{total}] {fname.name}")
        except Exception as e:
            print(f"  [{count}/{total}] ERROR for {key}: {e}")

    print(f"\n  wrote {total} PNGs")

    # Static reference figure
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    configs = [
        (1.0, 1.0, 0.5, "dirichlet"),
        (1.0, 1.0, 2.0, "dirichlet"),
        (1.0, 1.0, 4.0, "dirichlet"),
        (1.0, 1.0, 2.0, "neumann"),
        (2.0, 1.0, 2.0, "dirichlet"),
        (1.0, 3.0, 2.0, "dirichlet"),
    ]
    for idx, (a, k, s, bc) in enumerate(configs):
        ax = axes[idx // 3][idx % 3]
        samples = _samples_for_params(a, k, s, bc, M, x)
        for kk in range(samples.shape[0]):
            ax.plot(x, samples[kk], lw=1.5, alpha=0.7)
        ax.set_title(f"α={a}, κ={k}, s={s}, {bc}", fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("m(x)")
    fig.tight_layout()
    save(fig, "f6f_overview", out_dir)
    print("  wrote f6f_overview.png/svg")


if __name__ == "__main__":
    main()
