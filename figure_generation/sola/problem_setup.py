"""Shared problem setup for the "My Take on SOLA" figures.

Defines a 1-D linear inverse problem on ``[0, 1]`` with:
- a forward operator ``G`` with Gaussian sensitivity kernels,
- a target operator ``T`` with localized averaging target kernels,
- the SOLA matrix ``X`` (noiseless and noise-aware, constrained and unconstrained),
- resolving kernels, propagated covariance, and a cautionary-tale true model.

Uses the ``intervalinf`` / ``pygeoinf`` stack from the ``inferences`` conda env.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from intervalinf import IntervalDomain, Lebesgue, Function
from intervalinf.operators import SOLAOperator
from intervalinf.providers import BumpFunctionProvider, NormalModesProvider
from pygeoinf import EuclideanSpace

# ---------------------------------------------------------------------------
# Fixed problem parameters
# ---------------------------------------------------------------------------

DOMAIN: tuple[float, float] = (0.0, 1.0)
N_D: int = 20                       # number of data
N_P: int = 15                       # number of target properties
KERNEL_WIDTH: float = 0.07          # Gaussian sensitivity-kernel width (unused for normal modes)
TARGET_WIDTH: float = 0.05          # Gaussian target-kernel width
NOISE_FRAC: float = 0.10            # data noise as fraction of max|d|
SEED: int = 42
KERNEL_SEED: int = 7               # random seed for normal-mode kernel generation


def kernel_centers(n_d: int = N_D) -> np.ndarray:
    """Staggered depths at which sensitivity kernels are centred."""
    return np.linspace(DOMAIN[0] + 0.12, DOMAIN[1] - 0.12, n_d)


def target_centers(n_p: int = N_P) -> np.ndarray:
    """Locations at which target averaging kernels are centred."""
    return np.linspace(DOMAIN[0] + 0.10, DOMAIN[1] - 0.10, n_p)


# ---------------------------------------------------------------------------
# Continuous (function-space) objects
# ---------------------------------------------------------------------------


def make_model_space() -> Lebesgue:
    """Return the continuous model space ``L2([0, 1])``."""
    return Lebesgue(0, IntervalDomain(*DOMAIN), basis=None)


def make_forward(model_space: Lebesgue, n_d: int = N_D) -> SOLAOperator:
    """Build the forward operator with realistic normal-mode sensitivity kernels.

    Uses :class:`NormalModesProvider` to generate kernels that resemble
    oscillatory sensitivity functions (e.g. seismic normal modes, helioseismic
    eigenfunctions) rather than simple Gaussian bumps.
    """
    provider = NormalModesProvider(
        model_space,
        random_state=KERNEL_SEED,
        n_modes_range=(3, 6),
        coeff_range=(-2.0, 2.0),
        freq_range=(1.0, 8.0),
        gaussian_width_percent_range=(10.0, 40.0),
    )
    kernels = [provider.get_function_by_index(i) for i in range(n_d)]
    return SOLAOperator(model_space, EuclideanSpace(n_d), kernels=kernels)


def make_target(model_space: Lebesgue, n_p: int = N_P) -> SOLAOperator:
    """Build the target property operator with localized averaging kernels.

    The BumpFunctionProvider creates unit-area Gaussian bumps, so each
    target property is a localised average of the model.
    """
    centers = target_centers(n_p)
    provider = BumpFunctionProvider(
        model_space, centers=centers, default_width=TARGET_WIDTH,
    )
    return SOLAOperator(model_space, EuclideanSpace(n_p), kernels=provider)


def true_model(model_space: Lebesgue) -> Function:
    """A smooth true model with structure at multiple scales.

    Includes a low-frequency component well-resolved by the data kernels
    and a higher-frequency component that is partially invisible to G
    but visible to the target kernels — the cautionary-tale ingredient.
    """

    def f(x: np.ndarray) -> np.ndarray:
        return (
            0.5
            + 0.3 * np.sin(2 * np.pi * x)
            + 0.2 * np.exp(-((x - 0.35) / 0.04) ** 2)
            + 0.15 * np.sin(8 * np.pi * x)  # high-freq: visible to T, not to G
        )

    return Function(model_space, evaluate_callable=f)


def true_model_smooth(model_space: Lebesgue) -> Function:
    """A smooth true model without the hidden high-frequency component.

    Used for contrast in the cautionary tale.
    """

    def f(x: np.ndarray) -> np.ndarray:
        return (
            0.5
            + 0.3 * np.sin(2 * np.pi * x)
            + 0.2 * np.exp(-((x - 0.35) / 0.04) ** 2)
        )

    return Function(model_space, evaluate_callable=f)


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------


@dataclass
class Data:
    """Synthetic data bundle."""

    d: np.ndarray              # noisy observations
    d_clean: np.ndarray        # noise-free G(m_bar)
    noise_std: float           # scalar noise standard deviation
    cov: np.ndarray            # data-noise covariance matrix


def make_data(
    forward: SOLAOperator,
    m_bar: Function,
    *,
    noise_frac: float = NOISE_FRAC,
    seed: int = SEED,
) -> Data:
    """Generate noisy data ``d = G(m_bar) + eta`` with diagonal noise covariance."""
    d_clean = forward(m_bar)
    noise_std = float(noise_frac * np.max(np.abs(d_clean)))
    rng = np.random.default_rng(seed)
    d = d_clean + rng.normal(0.0, noise_std, d_clean.shape)
    n_d = d_clean.shape[0]
    cov = (noise_std ** 2) * np.eye(n_d)
    return Data(d=d, d_clean=d_clean, noise_std=noise_std, cov=cov)


# ---------------------------------------------------------------------------
# SOLA matrix computation
# ---------------------------------------------------------------------------


def gram_data(forward: SOLAOperator) -> np.ndarray:
    """Data-space Gram matrix ``H = G G*`` (N_d x N_d)."""
    return forward.compute_gram_matrix()


def target_forward_cross(target: SOLAOperator, forward: SOLAOperator) -> np.ndarray:
    """Cross-gram ``T G*`` (N_p x N_d)."""
    return target.compute_cross_gram_matrix(forward)


def sola_matrix_noiseless(
    forward: SOLAOperator,
    target: SOLAOperator,
) -> np.ndarray:
    """Unconstrained noiseless SOLA matrix: ``X_0 = T G* (G G*)^{-1}``."""
    H = gram_data(forward)
    TG = target_forward_cross(target, forward)
    return TG @ np.linalg.inv(H)


def sola_matrix_noisy(
    forward: SOLAOperator,
    target: SOLAOperator,
    data: Data,
) -> np.ndarray:
    """Unconstrained noise-aware SOLA matrix: ``X_0 = T G* (G G* + C_D)^{-1}``."""
    H = gram_data(forward)
    M = H + data.cov
    TG = target_forward_cross(target, forward)
    return TG @ np.linalg.inv(M)


def sola_matrix_constrained_noiseless(
    forward: SOLAOperator,
    target: SOLAOperator,
) -> np.ndarray:
    """Constrained noiseless SOLA with unit-mass resolving kernels.

    Constraint: X v = w, where v = G(1) (forward of constant model)
    and w = T(1) = 1 for all k (since target kernels are unit-area averages).

    X_c = X_0 - (X_0 v - w) u* / beta
    where u = H^{-1} v, beta = <v, u>_D.
    """
    H = gram_data(forward)
    TG = target_forward_cross(target, forward)
    X0 = TG @ np.linalg.inv(H)

    model_space = forward.domain
    ones_model = Function(model_space, evaluate_callable=lambda x: np.ones_like(x))
    v = forward(ones_model)
    w = target(ones_model)  # should be ~1 for unit-area targets

    u = np.linalg.solve(H, v)
    beta = float(v @ u)
    lam = (X0 @ v - w) / beta
    Xc = X0 - np.outer(lam, u)
    return Xc


def sola_matrix_constrained_noisy(
    forward: SOLAOperator,
    target: SOLAOperator,
    data: Data,
) -> np.ndarray:
    """Constrained noise-aware SOLA with unit-mass resolving kernels."""
    H = gram_data(forward)
    M = H + data.cov
    TG = target_forward_cross(target, forward)
    X0 = TG @ np.linalg.inv(M)

    model_space = forward.domain
    ones_model = Function(model_space, evaluate_callable=lambda x: np.ones_like(x))
    v = forward(ones_model)
    w = target(ones_model)

    u = np.linalg.solve(M, v)
    beta = float(v @ u)
    lam = (X0 @ v - w) / beta
    Xc = X0 - np.outer(lam, u)
    return Xc


# ---------------------------------------------------------------------------
# Resolving kernels and property estimates
# ---------------------------------------------------------------------------


def resolving_kernel(
    forward: SOLAOperator,
    X: np.ndarray,
    k: int,
    x: np.ndarray,
) -> np.ndarray:
    """Evaluate the k-th resolving kernel R_k(r) = sum_i X_ki K_i(r) on grid x."""
    n_d = forward.codomain.dim
    vals = np.zeros_like(x)
    for i in range(n_d):
        ki = forward.get_kernel(i)
        vals += X[k, i] * ki.evaluate(x)
    return vals


def target_kernel_eval(
    target: SOLAOperator,
    k: int,
    x: np.ndarray,
) -> np.ndarray:
    """Evaluate the k-th target kernel T^(k)(r) on grid x."""
    return target.get_kernel(k).evaluate(x)


def sola_estimates(X: np.ndarray, data: Data) -> np.ndarray:
    """SOLA property estimates: p_tilde = X d_tilde."""
    return X @ data.d


def propagated_covariance(X: np.ndarray, data: Data) -> np.ndarray:
    """Propagated data-noise covariance: C_P = X C_D X*."""
    return X @ data.cov @ X.T


def true_target_properties(target: SOLAOperator, m_bar: Function) -> np.ndarray:
    """Exact target properties: p_bar = T(m_bar)."""
    return target(m_bar)


def resolved_properties(X: np.ndarray, forward: SOLAOperator, m_bar: Function) -> np.ndarray:
    """Noiseless resolved properties: A(m_bar) = X G(m_bar)."""
    return X @ forward(m_bar)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def output_dir() -> Path:
    """``<repo>/media/research/sola`` (created if missing)."""
    repo_root = Path(__file__).resolve().parents[2]
    out = repo_root / "media" / "research" / "sola"
    out.mkdir(parents=True, exist_ok=True)
    return out


def plot_grid(n: int = 1000) -> np.ndarray:
    """Dense evaluation grid over the domain for smooth curves."""
    return np.linspace(DOMAIN[0], DOMAIN[1], n)


# ---------------------------------------------------------------------------
# Convenience: build everything at once
# ---------------------------------------------------------------------------


@dataclass
class SOLAProblem:
    """All objects needed for figure generation."""

    model_space: Lebesgue
    forward: SOLAOperator
    target: SOLAOperator
    m_bar: Function
    m_bar_smooth: Function
    data: Data
    X_noiseless: np.ndarray
    X_noisy: np.ndarray
    X_constrained_noiseless: np.ndarray
    X_constrained_noisy: np.ndarray
    x: np.ndarray


def make_problem() -> SOLAProblem:
    """Build the full SOLA problem with all matrix variants."""
    model_space = make_model_space()
    forward = make_forward(model_space)
    target = make_target(model_space)
    m_bar = true_model(model_space)
    m_bar_smooth = true_model_smooth(model_space)
    data = make_data(forward, m_bar)
    x = plot_grid()

    X_noiseless = sola_matrix_noiseless(forward, target)
    X_noisy = sola_matrix_noisy(forward, target, data)
    X_constrained_noiseless = sola_matrix_constrained_noiseless(forward, target)
    X_constrained_noisy = sola_matrix_constrained_noisy(forward, target, data)

    return SOLAProblem(
        model_space=model_space,
        forward=forward,
        target=target,
        m_bar=m_bar,
        m_bar_smooth=m_bar_smooth,
        data=data,
        X_noiseless=X_noiseless,
        X_noisy=X_noisy,
        X_constrained_noiseless=X_constrained_noiseless,
        X_constrained_noisy=X_constrained_noisy,
        x=x,
    )


if __name__ == "__main__":
    prob = make_problem()
    print(f"N_d={N_D}  N_p={N_P}  noise_std={prob.data.noise_std:.4e}")
    print(f"X_noiseless shape: {prob.X_noiseless.shape}")
    print(f"X_constrained_noisy shape: {prob.X_constrained_noisy.shape}")

    # Quick sanity: resolving kernel masses for constrained vs unconstrained
    for k in [0, N_P // 2, N_P - 1]:
        rk_unc = resolving_kernel(prob.forward, prob.X_noisy, k, prob.x)
        rk_con = resolving_kernel(prob.forward, prob.X_constrained_noisy, k, prob.x)
        mass_unc = np.trapezoid(rk_unc, prob.x)
        mass_con = np.trapezoid(rk_con, prob.x)
        print(f"  k={k}: unconstrained mass={mass_unc:.4f}  constrained mass={mass_con:.4f}")
