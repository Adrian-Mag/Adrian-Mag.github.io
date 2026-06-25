"""Figure F6e - Covariance operator as a spectral filter.

Pre-computes KL expansion samples using intervalinf's BesselSobolevInverse
for s in {0, 0.5, 1.0, ..., 6.0}.  For each s, draws 3 sample paths on a
dense grid and saves them as transparent PNGs.

Output: media/research/think-first/f6e_s{VALUE}.png  (one per s value)
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

from intervalinf import IntervalDomain, Lebesgue
from intervalinf.operators import BesselSobolevInverse, Laplacian
from intervalinf.core.boundary import BoundaryConditions
from intervalinf.sampling import KLSampler

from style import apply_style, mako_light_n, plt, save
from problem_setup import output_dir, DOMAIN

S_VALUES = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
N_SAMPLES = 3
N_MODES = 80
N_GRID = 500
KAPPA = 1.0
SEED = 42


def _compute_trace(s: float, n_modes: int = N_MODES) -> float:
    trace = 0.0
    for j in range(1, n_modes + 1):
        rho_j = (j * np.pi) ** 2
        lam = (KAPPA ** 2 + rho_j) ** (-s)
        trace += lam
    return trace


def _make_covariance(s: float, M: Lebesgue):
    lap = Laplacian(
        M, BoundaryConditions.dirichlet(), 1.0,
        method="spectral", dofs=120,
    )
    return BesselSobolevInverse(
        M, M, KAPPA, s, lap,
        dofs=120, n_samples=N_SAMPLES, use_fast_transforms=True,
    )


def _samples_for_s(s: float, M: Lebesgue, x: np.ndarray) -> np.ndarray:
    cov = _make_covariance(s, M)
    sampler = KLSampler(cov, n_modes=N_MODES, rng=np.random.default_rng(SEED))
    samples = sampler.samples(N_SAMPLES)
    return np.asarray(
        [np.asarray(f.evaluate(x), dtype=float) for f in samples],
        dtype=float,
    )


def _save_panel_png(samples, x, out_path):
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    colors = mako_light_n(N_SAMPLES)
    for k in range(samples.shape[0]):
        ax.plot(x, samples[k], color=colors[k], lw=1.5, alpha=0.7)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel(r"$m(x) - m_0$", fontsize=10)
    ax.tick_params(labelsize=8)
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

    for s in S_VALUES:
        samples = _samples_for_s(s, M, x)
        fname = out_dir / f"f6e_s{s:.1f}.png"
        _save_panel_png(samples, x, fname)
        trace = _compute_trace(s)
        trace_str = f"{trace:.4f}" if s > 0.5 else "→ ∞"
        print(f"  s={s:.1f}: wrote {fname.name}, trace={trace_str}")

    # Static overview figure
    fig, axes = plt.subplots(3, 3, figsize=(12, 9))
    s_plot = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
    colors = mako_light_n(N_SAMPLES)
    for idx, s in enumerate(s_plot):
        ax = axes[idx // 3][idx % 3]
        samples = _samples_for_s(s, M, x)
        for k in range(samples.shape[0]):
            ax.plot(x, samples[k], color=colors[k], lw=1.5, alpha=0.7)
        ax.set_title(f"s = {s}", fontsize=12)
        ax.set_xlabel("x")
        ax.set_ylabel(r"$m(x) - m_0$")
    axes[2][2].set_visible(False)
    fig.tight_layout()
    save(fig, "f6e_overview", out_dir)
    print("  wrote f6e_overview.png/svg")


if __name__ == "__main__":
    main()
