"""Figure script for Act 7: A Synthetic Cautionary Tale.

Reproduces the SOLA failure demonstration from the original notebook,
adapted for the website's dark-theme styling.

Narrative flow:
1. A standard SOLA problem (data, kernels, targets)
2. SOLA solution looks good (nice resolving kernels, reasonable estimates)
3. THE REVEAL: true target properties are the negative of SOLA estimates
4. The true model looks wild (large norm, rapid oscillations)

The key construction: given a normal model m_n with data d = G(m_n) and
properties p = T(m_n), we build a pathological model m_path satisfying
    G(m_path) = d,        T(m_path) = -p.
Both models produce identical data, but their target properties are opposites.
SOLA, which only sees the data, produces estimates close to p — and therefore
approximately the negative of the true target properties T(m_path).

Generates:
- fig_act7_data.png: Observed data with error bars
- fig_act7_resolving.png: Resolving kernels vs target kernels (looks good)
- fig_act7_sola_good.png: SOLA estimates with 2-sigma uncertainty (looks good)
- fig_act7_reveal.png: THE REVEAL — estimates vs true (negative) properties
- fig_act7_true_model.png: Pathological true model vs least-norm solution
"""

from __future__ import annotations

import numpy as np

from style import PALETTE, apply_style, mako_light_n, plt, save
from problem_setup import (
    make_model_space,
    plot_grid,
    output_dir,
    resolving_kernel,
    target_kernel_eval,
    DOMAIN,
    NOISE_FRAC,
    SEED,
)
from problem_setup import Data
from intervalinf import IntervalDomain, Lebesgue, Function
from intervalinf.operators import SOLAOperator
from intervalinf.providers import BumpFunctionProvider, NormalModesProvider
from pygeoinf import EuclideanSpace

apply_style()

# Act-7-specific problem parameters (larger than the shared setup, matching
# the original notebook so that resolving kernels look genuinely good).
N_D = 100
N_P = 20
TARGET_WIDTH = 0.2
KERNEL_SEED = 2


def make_forward_act7(model_space: Lebesgue) -> SOLAOperator:
    """Forward operator with rich normal-mode kernels (N_D=100)."""
    provider = NormalModesProvider(
        model_space,
        n_modes_range=(1, 50),
        coeff_range=(-5, 5),
        gaussian_width_percent_range=(1, 5),
        freq_range=(0.1, 20),
        random_state=KERNEL_SEED,
    )
    kernels = [provider.get_function_by_index(i) for i in range(N_D)]
    return SOLAOperator(model_space, EuclideanSpace(N_D), kernels=kernels)


def make_target_act7(model_space: Lebesgue) -> SOLAOperator:
    """Target operator with localized bump averages (N_P=20)."""
    centers = np.linspace(DOMAIN[0] + TARGET_WIDTH / 2, DOMAIN[1] - TARGET_WIDTH / 2, N_P)
    provider = BumpFunctionProvider(
        model_space, centers=centers, default_width=TARGET_WIDTH,
    )
    return SOLAOperator(model_space, EuclideanSpace(N_P), kernels=provider)


def normal_model(model_space: Lebesgue) -> Function:
    """A smooth, moderate-norm model used to generate data."""
    def f(x):
        return np.exp(-((x - 0.5) / 0.5) ** 2) * np.sin(5 * np.pi * x) + x
    return Function(model_space, evaluate_callable=f)


def sola_constrained_noisy(G, T, d_tilde, C_D):
    """Constrained noise-aware SOLA matrix with unimodularity."""
    GG = G.compute_gram_matrix()
    M = GG + C_D
    TG = T.compute_cross_gram_matrix(G)
    X0 = TG @ np.linalg.inv(M)

    ones = Function(G.domain, evaluate_callable=lambda x: np.ones_like(x))
    v = G(ones)
    w = T(ones)
    u = np.linalg.solve(M, v)
    beta = float(v @ u)
    lam = (X0 @ v - w) / beta
    return X0 - np.outer(lam, u)


def main() -> None:
    # --- Build problem ---
    M = make_model_space()
    G = make_forward_act7(M)
    T = make_target_act7(M)
    x = plot_grid()
    centers = np.linspace(DOMAIN[0] + TARGET_WIDTH / 2, DOMAIN[1] - TARGET_WIDTH / 2, N_P)

    # --- Normal model and data ---
    m_normal = normal_model(M)
    d_bar = G(m_normal)
    p_normal = T(m_normal)

    noise_std = NOISE_FRAC * np.max(np.abs(d_bar))
    rng = np.random.default_rng(SEED)
    d_tilde = d_bar + rng.normal(0, noise_std, d_bar.shape)
    C_D = noise_std ** 2 * np.eye(N_D)

    data = Data(d=d_tilde, d_clean=d_bar, noise_std=noise_std, cov=C_D)

    # --- SOLA solution (constrained, noise-aware) ---
    X_c = sola_constrained_noisy(G, T, d_tilde, C_D)
    p_sola = X_c @ d_tilde
    C_P = X_c @ C_D @ X_c.T
    p_std = np.sqrt(np.diag(C_P))

    # --- Pathological model ---
    # Solve: G(m) = d_bar, T(m) = -p_normal  via minimum-norm solution
    # using the stacked operator [G; T].
    GG = G.compute_gram_matrix()
    GT = G.compute_cross_gram_matrix(T)
    TT = T.compute_gram_matrix()

    stacked_gram = np.block([[GG, GT], [GT.T, TT]])
    rhs = np.concatenate([d_bar, -p_normal])
    coeffs, _, _, _ = np.linalg.lstsq(stacked_gram, rhs, rcond=None)

    coeffs_d = coeffs[:N_D]
    coeffs_p = coeffs[N_D:]

    def m_path_eval(x_eval):
        val = np.zeros_like(x_eval, dtype=float)
        for i in range(N_D):
            val += coeffs_d[i] * G.get_kernel(i).evaluate(x_eval)
        for k in range(N_P):
            val += coeffs_p[k] * T.get_kernel(k).evaluate(x_eval)
        return val

    m_pathological = Function(M, evaluate_callable=m_path_eval)
    p_true = T(m_pathological)

    # --- Least-norm solution (what SOLA implicitly assumes) ---
    M_mat = GG + C_D
    M_inv_d = np.linalg.solve(M_mat, d_tilde)

    def m_least_eval(x_eval):
        val = np.zeros_like(x_eval, dtype=float)
        for i in range(N_D):
            val += M_inv_d[i] * G.get_kernel(i).evaluate(x_eval)
        return val

    m_least = Function(M, evaluate_callable=m_least_eval)

    # --- Verification ---
    print(f"Normal model norm:       {M.norm(m_normal):.4f}")
    print(f"Pathological model norm: {M.norm(m_pathological):.4f}")
    print(f"Least-norm model norm:   {M.norm(m_least):.4f}")
    print(f"Data fit error:          {np.linalg.norm(G(m_pathological) - d_bar):.2e}")
    print(f"Property error:          {np.linalg.norm(T(m_pathological) - (-p_normal)):.2e}")
    print(f"SOLA estimates:          min={np.min(p_sola):.4f}, max={np.max(p_sola):.4f}")
    print(f"True properties:         min={np.min(p_true):.4f}, max={np.max(p_true):.4f}")
    print(f"Correlation(p_sola, p_true): {np.corrcoef(p_sola, p_true)[0, 1]:.4f}")

    # Resolving kernel misfits
    misfits = np.zeros(N_P)
    for k in range(N_P):
        rk = resolving_kernel(G, X_c, k, x)
        tk = target_kernel_eval(T, k, x)
        misfits[k] = np.sqrt(np.trapezoid((rk - tk) ** 2, x)) / np.sqrt(np.trapezoid(tk ** 2, x))
    print(f"Resolving kernel misfit: avg={100*np.mean(misfits):.1f}%, max={100*np.max(misfits):.1f}%")

    out = output_dir()

    # --- Figure 1: Observed data ---
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.scatter(range(N_D), d_tilde, color=PALETTE["data"], s=20, zorder=5)
    ax.errorbar(
        range(N_D), d_tilde, yerr=noise_std,
        fmt="none", color=PALETTE["data"], alpha=0.5, capsize=2,
    )
    ax.set_xlabel("Observation index")
    ax.set_ylabel("Data value")
    ax.set_title("Observed data with measurement uncertainty")
    save(fig, "fig_act7_data", out)

    # --- Figure 2: Resolving vs target kernels ---
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = mako_light_n(N_P)
    for k in range(N_P):
        tk = target_kernel_eval(T, k, x)
        ax.plot(x, tk, color=PALETTE["true"], alpha=0.3, lw=3)
    for k in range(N_P):
        rk = resolving_kernel(G, X_c, k, x)
        ax.plot(x, rk, color=colors[k], alpha=0.9, lw=2)
    ax.plot([], [], color=PALETTE["true"], alpha=0.5, lw=3, label="Target kernels")
    ax.plot([], [], color=colors[N_P // 2], alpha=0.9, lw=2, label="Resolving kernels")
    ax.legend()
    ax.set_xlabel(r"$r$")
    ax.set_ylabel("Kernel value")
    ax.set_title("Resolving kernels vs. target kernels")
    save(fig, "fig_act7_resolving", out)

    # --- Figure 3: SOLA estimates (looks good) ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(centers, p_sola, color=PALETTE["mako_dark"], s=80, zorder=5)
    ax.fill_between(
        centers, p_sola - 2 * p_std, p_sola + 2 * p_std,
        alpha=0.25, color=PALETTE["mako_dark"],
    )
    ax.errorbar(
        centers, p_sola, yerr=2 * p_std,
        fmt="none", color=PALETTE["mako_dark"], alpha=0.6, capsize=3,
    )
    ax.axhline(0, color=PALETTE["muted"], ls="--", alpha=0.5)
    ax.set_xlabel("Target location")
    ax.set_ylabel("Property value")
    ax.set_title("SOLA property estimates with uncertainty")
    save(fig, "fig_act7_sola_good", out)

    # --- Figure 4: THE REVEAL ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(
        centers, p_sola, color=PALETTE["mako_dark"], s=80, zorder=5,
        label="SOLA estimates",
    )
    ax.fill_between(
        centers, p_sola - 2 * p_std, p_sola + 2 * p_std,
        alpha=0.25, color=PALETTE["mako_dark"],
    )
    ax.errorbar(
        centers, p_sola, yerr=2 * p_std,
        fmt="none", color=PALETTE["mako_dark"], alpha=0.6, capsize=3,
    )
    ax.scatter(
        centers, p_true, color=PALETTE["naive"], marker="x", s=120,
        linewidths=3, zorder=10, label="True target properties",
    )
    ax.axhline(0, color=PALETTE["muted"], ls="--", alpha=0.5)
    ax.legend()
    ax.set_xlabel("Target location")
    ax.set_ylabel("Property value")
    ax.set_title("SOLA estimates vs. true target properties")
    save(fig, "fig_act7_reveal", out)

    # --- Figure 5: The true model ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        x, m_pathological.evaluate(x),
        color=PALETTE["naive"], lw=2,
        label=f"True model (pathological, $\\|m\\|$={M.norm(m_pathological):.0f})",
    )
    ax.plot(
        x, m_least.evaluate(x),
        color=PALETTE["mako_dark"], lw=2, ls="--",
        label=f"Least-norm solution ($\\|m\\|$={M.norm(m_least):.1f})",
    )
    ax.plot(
        x, m_normal.evaluate(x),
        color=PALETTE["true"], lw=1.5, alpha=0.5,
        label=f"Normal model ($\\|m\\|$={M.norm(m_normal):.1f})",
    )
    ax.legend()
    ax.set_xlabel(r"$r$")
    ax.set_ylabel("Model value")
    ax.set_title("The true model vs. what SOLA implicitly assumes")
    save(fig, "fig_act7_true_model", out)


if __name__ == "__main__":
    main()
