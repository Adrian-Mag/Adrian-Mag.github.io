"""Shared problem setup for the "Think First, Discretize Later" figures.

This module defines ONE small 1-D linear inverse problem and the discretisation
machinery used by every figure on the explainer page. It is offline tooling: it
imports ``intervalinf``/``pygeoinf`` (from the ``inferences`` conda env) and is
**not** part of the served static website.

The narrative spine the figures illustrate:

* The forward problem lives in a function space ``M = L2([0, 1])``; data are a
  handful of weighted integrals (a SOLA operator).
* A "naive" discretisation treats the coefficient vector as if it lived in a
  plain Euclidean space, so the adjoint becomes the matrix transpose ``G^T``.
* The geometry-correct discretisation equips the coefficient space with the
  basis Gram (mass) matrix ``M``, so the adjoint is ``G* = M^-1 G^T``.
* With overlapping hat functions ``M`` is tridiagonal and non-diagonal, so
  naive != correct — the transpose is not the adjoint.

Run ``python problem_setup.py`` to print the headline naive-vs-correct numbers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

import numpy as np

from intervalinf import IntervalDomain, Lebesgue, Function
from intervalinf.operators import (
    SOLAOperator,
    InverseLaplacian,
    BesselSobolevInverse,
    Laplacian,
)
from intervalinf.providers import (
    BumpFunctionProvider,
    BoxCarFunctionProvider,
    HatFunctionProvider,
    CustomBasisProvider,
)
from intervalinf.core.boundary import BoundaryConditions
from intervalinf.sampling import KLSampler
from pygeoinf import (
    EuclideanSpace,
    LinearOperator,
    CholeskySolver,
    GaussianMeasure,
    MassWeightedHilbertSpace,
)
from pygeoinf.forward_problem import LinearForwardProblem
from pygeoinf.linear_bayesian import LinearBayesianInversion

# ---------------------------------------------------------------------------
# Fixed problem parameters (shared by every figure for visual consistency)
# ---------------------------------------------------------------------------

DOMAIN: tuple[float, float] = (0.0, 1.0)
N_D: int = 20                      # number of data (integral measurements)
KERNEL_WIDTH: float = 0.07          # Gaussian sensitivity-kernel width
NOISE_FRAC: float = 0.10           # data noise as a fraction of max|d|
SEED: int = 0

BasisKind = Literal["box", "hat"]


def kernel_centers(n_d: int = N_D) -> np.ndarray:
    """Staggered depths at which the sensitivity kernels are centred."""
    return np.linspace(DOMAIN[0] + 0.12, DOMAIN[1] - 0.12, n_d)


# ---------------------------------------------------------------------------
# Continuous (function-space) problem
# ---------------------------------------------------------------------------


def make_model_space() -> Lebesgue:
    """Return the continuous, basis-free model space ``L2([0, 1])``."""
    return Lebesgue(0, IntervalDomain(*DOMAIN), basis=None)


def make_forward(model_space: Lebesgue, n_d: int = N_D) -> SOLAOperator:
    """Build the SOLA forward operator with smooth Gaussian sensitivity kernels."""
    provider = BumpFunctionProvider(
        model_space, centers=kernel_centers(n_d), default_width=KERNEL_WIDTH
    )
    return SOLAOperator(model_space, EuclideanSpace(n_d), kernels=provider)


def true_model(model_space: Lebesgue) -> Function:
    """A smooth-but-structured true model: two Gaussian bumps plus a gentle ramp."""

    def f(x: np.ndarray) -> np.ndarray:
        return (
            np.exp(-((x - 0.30) / 0.08) ** 2)
            + 0.6 * np.exp(-((x - 0.65) / 0.06) ** 2)
            + 0.4 * x
        )

    return Function(model_space, evaluate_callable=f)


@dataclass
class Data:
    """Synthetic data bundle."""

    d: np.ndarray              # noisy observations
    d_clean: np.ndarray        # noise-free G(m_bar)
    noise_std: float           # scalar noise standard deviation
    measure: GaussianMeasure   # zero-mean data-noise measure on D


def make_data(
    forward: SOLAOperator,
    m_bar: Function,
    *,
    noise_frac: float = NOISE_FRAC,
    seed: int = SEED,
) -> Data:
    """Generate noisy data ``d = G(m_bar) + eta`` with a diagonal noise covariance."""
    d_clean = forward(m_bar)
    noise_std = float(noise_frac * np.max(np.abs(d_clean)))
    rng = np.random.default_rng(seed)
    d = d_clean + rng.normal(0.0, noise_std, d_clean.shape)
    data_space = forward.codomain
    measure = GaussianMeasure.from_covariance_matrix(
        data_space, (noise_std**2) * np.eye(data_space.dim),
        expectation=np.zeros(data_space.dim),
    )
    return Data(d=d, d_clean=d_clean, noise_std=noise_std, measure=measure)


def continuous_least_norm(
    forward: SOLAOperator, data: Data, *, solver: CholeskySolver | None = None
) -> Function:
    """Minimum-norm (in the L2 model norm) reconstruction in the continuous space."""
    solver = solver or CholeskySolver(galerkin=True)
    gram = forward @ forward.adjoint
    inv = solver(gram + data.measure.covariance)
    return (forward.adjoint @ inv)(data.d)


# ---------------------------------------------------------------------------
# Discretisation: naive (Euclidean) vs geometry-correct (mass-weighted)
# ---------------------------------------------------------------------------


@dataclass
class Discretisation:
    """Holds the discrete spaces/operators for one basis at one resolution."""

    basis_kind: BasisKind
    n: int
    function_space: Lebesgue          # basis-backed model subspace M_N
    gram: np.ndarray                  # basis Gram / mass matrix (N x N)
    forward_matrix: np.ndarray        # G in the chosen basis (N_d x N)
    naive_forward: LinearOperator     # adjoint == G^T  (Euclidean coeff space)
    correct_forward: LinearOperator   # adjoint == M^-1 G^T (mass-weighted space)


def _build_basis_space(basis_kind: BasisKind, n: int) -> Lebesgue:
    domain = IntervalDomain(*DOMAIN)
    space = Lebesgue(n, domain, basis="none")
    if basis_kind == "box":
        edges = np.linspace(DOMAIN[0], DOMAIN[1], n + 1)
        centers = 0.5 * (edges[:-1] + edges[1:])
        widths = np.diff(edges)
        provider = BoxCarFunctionProvider(
            space, default_width=widths[0], centers=centers,
            normalize=False, default_height=1.0,
        )
        space.set_basis_provider(
            CustomBasisProvider(space, provider, orthonormal=False,
                                basis_type="cell-boxcar")
        )
    elif basis_kind == "hat":
        provider = HatFunctionProvider(space)
        space.set_basis_provider(
            CustomBasisProvider(space, provider, orthonormal=False,
                                basis_type="hat")
        )
    else:  # pragma: no cover - guarded by typing
        raise ValueError(f"unknown basis_kind {basis_kind!r}")
    return space


def discretise(
    forward: SOLAOperator, basis_kind: BasisKind, n: int
) -> Discretisation:
    """Project the continuous forward operator onto a basis at resolution ``n``.

    Returns both the *naive* operator (coefficient space is plain Euclidean, so
    its adjoint is the transpose ``G^T``) and the *correct* operator (coefficient
    space carries the Gram metric, so its adjoint is ``M^-1 G^T``).
    """
    data_space = forward.codomain
    n_d = data_space.dim
    space = _build_basis_space(basis_kind, n)
    discrete_forward = SOLAOperator(
        space, data_space,
        kernels=[forward.get_kernel(i) for i in range(n_d)],
        integration_config=forward.integration,
    )
    g_mat = discrete_forward.matrix(dense=True)
    n_basis = g_mat.shape[1]
    euclid = EuclideanSpace(n_basis)
    naive = LinearOperator.from_matrix(euclid, data_space, g_mat)

    gram = np.asarray(space.metric)
    mass = LinearOperator.self_adjoint_from_matrix(euclid, gram)
    inv_mass = LinearOperator.self_adjoint_from_matrix(euclid, np.linalg.inv(gram))
    weighted = MassWeightedHilbertSpace(euclid, mass, inv_mass)
    correct = LinearOperator.from_formal_adjoint(weighted, data_space, naive)

    return Discretisation(
        basis_kind=basis_kind, n=n, function_space=space, gram=gram,
        forward_matrix=g_mat, naive_forward=naive, correct_forward=correct,
    )


def least_norm_coefficients(
    operator: LinearOperator, data: Data, *, solver: CholeskySolver | None = None
) -> np.ndarray:
    """Minimum-norm coefficient vector for a discrete forward operator.

    The geometry enters only through ``operator.adjoint``: for the naive operator
    this is ``G^T``; for the correct operator it is ``M^-1 G^T``.
    """
    solver = solver or CholeskySolver(galerkin=True)
    gram = operator @ operator.adjoint
    inv = solver(gram + data.measure.covariance)
    return (operator.adjoint @ inv)(data.d)


def reconstruct(space: Lebesgue, coefficients: np.ndarray) -> Function:
    """Synthesise the function ``sum_i coeff_i phi_i`` from basis coefficients."""
    return space.from_components(coefficients)


# ---------------------------------------------------------------------------
# Proper covariance operators and prior samples (boundary-condition figure)
# ---------------------------------------------------------------------------

BC_FACTORIES: dict[str, Callable[[], BoundaryConditions]] = {
    "neumann": BoundaryConditions.neumann,
    "dirichlet": BoundaryConditions.dirichlet,
    "mixed_dn": BoundaryConditions.mixed_dirichlet_neumann,
    "mixed_nd": BoundaryConditions.mixed_neumann_dirichlet,
}


def proper_covariance(
    model_space: Lebesgue, bc_name: str, *, alpha: float = 0.02, dofs: int = 80
) -> InverseLaplacian:
    """A trace-class smoothing covariance ``(-alpha * Laplacian)^{-1}`` with BCs."""
    if bc_name not in BC_FACTORIES:
        raise ValueError(f"unknown bc_name {bc_name!r}; choose from {list(BC_FACTORIES)}")
    bc = BC_FACTORIES[bc_name]()
    return InverseLaplacian(model_space, bc, alpha, method="spectral", dofs=dofs)


def prior_samples(
    covariance: InverseLaplacian, *, n_samples: int = 4, n_modes: int = 24, seed: int = 1
) -> list[Function]:
    """Draw posterior-consistent prior realisations via a KL expansion."""
    sampler = KLSampler(covariance, n_modes=n_modes, rng=np.random.default_rng(seed))
    return sampler.samples(n_samples)


# ---------------------------------------------------------------------------
# Posterior under refinement (mirrors the EGU poster's fig10 method)
#
# The contrast here is the *prior*, solved with the real Bayesian machinery
# (``LinearBayesianInversion``) on a mass-weighted hat-function coefficient space:
#   * naive  : sigma * I  (a Euclidean identity — NOT trace-class as N grows),
#   * correct: a Bessel-Sobolev smoothing covariance (trace-class).
# As the hat resolution N increases, the naive posterior pointwise std grows
# without bound while the Bessel posterior converges.
# ---------------------------------------------------------------------------

REFINEMENT_DOFS: int = 500
REFINEMENT_BESSEL_N_SAMPLES: int = 16384
BESSEL_K: float = 0.1
BESSEL_S: float = 4.0
BESSEL_AMPLITUDE: float = 100.0   # scales the Bessel prior so its band is visible
NAIVE_SIGMA: float = 1.0          # amplitude of the naive sigma*I prior
POSTERIOR_SAMPLES: int = 60

PriorKind = Literal["naive", "bessel"]


@dataclass
class CoeffSpace:
    """A hat-function model subspace plus its mass-weighted coeff space."""

    n: int
    function_space: Lebesgue
    coeff_space: MassWeightedHilbertSpace   # carries the Gram metric
    euclidean: EuclideanSpace               # underlying (un-weighted) coeffs


def _psd_clip(matrix: np.ndarray, rel: float = 1e-8) -> np.ndarray:
    """Symmetrise and project onto the PSD cone (clip discretisation negatives)."""
    sym = 0.5 * (matrix + matrix.T)
    evals, evecs = np.linalg.eigh(sym)
    floor = rel * max(float(evals.max()), 0.0)
    evals = np.clip(evals, floor, None)
    return (evecs * evals) @ evecs.T


def make_bessel_covariance(
    model_space: Lebesgue,
    *,
    dofs: int = REFINEMENT_DOFS,
    n_samples: int = REFINEMENT_BESSEL_N_SAMPLES,
) -> BesselSobolevInverse:
    """Trace-class Bessel-Sobolev smoothing covariance with Dirichlet BCs."""
    length = DOMAIN[1] - DOMAIN[0]
    laplacian = Laplacian(
        model_space, BoundaryConditions.dirichlet(), length,
        method="spectral", dofs=dofs,
    )
    return BesselSobolevInverse(
        model_space, model_space, BESSEL_K, BESSEL_S, laplacian,
        dofs=dofs, n_samples=n_samples, use_fast_transforms=True,
    )


def hat_coeff_space(n: int) -> CoeffSpace:
    """Build the hat-function space and its mass-weighted coefficient space."""
    domain = IntervalDomain(*DOMAIN)
    space = Lebesgue(n, domain, basis="none")
    space.integration_method = "simpson"
    space.integration_npoints = 4000
    provider = HatFunctionProvider(space)
    space.set_basis_provider(
        CustomBasisProvider(space, provider, orthonormal=False, basis_type="hat")
    )
    gram = np.asarray(space.metric)
    euclid = EuclideanSpace(n)
    mass = LinearOperator.from_matrix(euclid, euclid, gram)
    inv_mass = LinearOperator.from_matrix(euclid, euclid, np.linalg.inv(gram))
    coeff_space = MassWeightedHilbertSpace(euclid, mass, inv_mass)
    return CoeffSpace(n=n, function_space=space, coeff_space=coeff_space,
                     euclidean=euclid)


def data_error_measure(data: Data, data_space: EuclideanSpace) -> GaussianMeasure:
    """Diagonal data-noise measure consistent with :func:`make_data`."""
    return GaussianMeasure.from_standard_deviation(
        data_space, data.noise_std, expectation=np.zeros(data_space.dim),
    )


def discrete_prior(
    kind: PriorKind,
    box: CoeffSpace,
    *,
    bessel_covariance: BesselSobolevInverse | None = None,
) -> GaussianMeasure:
    """Galerkin-projected discrete prior on the mass-weighted coefficient space."""
    if kind == "naive":
        raw = NAIVE_SIGMA * box.euclidean.identity_operator()
    elif kind == "bessel":
        if bessel_covariance is None:
            raise ValueError("bessel prior requires a bessel_covariance")
        raw = BESSEL_AMPLITUDE * (
            box.function_space.coordinate_projection
            @ bessel_covariance
            @ box.function_space.coordinate_inclusion
        )
    else:  # pragma: no cover
        raise ValueError(f"unknown prior kind {kind!r}")
    weighted = LinearOperator.from_formally_self_adjoint(box.coeff_space, raw)
    cov = _psd_clip(weighted.matrix(dense=True, galerkin=True))
    return GaussianMeasure.from_covariance_matrix(
        box.coeff_space, cov, expectation=box.coeff_space.zero,
    )


@dataclass
class PosteriorCurves:
    """Posterior summary on a plotting grid."""

    x: np.ndarray
    mean: np.ndarray
    std: np.ndarray


def posterior_curves(
    forward: SOLAOperator,
    data: Data,
    box: CoeffSpace,
    prior: GaussianMeasure,
    x: np.ndarray,
    *,
    n_samples: int = POSTERIOR_SAMPLES,
) -> PosteriorCurves:
    """Bayesian posterior mean and pointwise std for a discrete prior."""
    data_space = forward.codomain
    g_discrete = LinearOperator.from_formal_adjoint(
        box.coeff_space, data_space,
        forward @ box.function_space.coordinate_inclusion,
    )
    problem = LinearForwardProblem(g_discrete, data_error_measure=data_error_measure(data, data_space))
    inversion = LinearBayesianInversion(problem, prior, formalism="data_space")
    posterior = inversion.model_posterior_measure(data.d, CholeskySolver())
    mean = np.asarray(box.function_space.from_components(posterior.expectation).evaluate(x), float)
    samples = np.asarray(
        [np.asarray(box.function_space.from_components(posterior.sample()).evaluate(x), float)
         for _ in range(n_samples)],
        dtype=float,
    )
    return PosteriorCurves(x=x, mean=mean, std=samples.std(axis=0))


REFINEMENT_NS: tuple[int, ...] = (10, 20, 30, 40, 50)


@dataclass
class RefinementResult:
    """Naive vs Bessel posteriors across a range of hat-function resolutions."""

    x: np.ndarray
    true_vals: np.ndarray
    ns: tuple[int, ...]
    naive: dict[int, PosteriorCurves]
    bessel: dict[int, PosteriorCurves]
    data: Data


def compute_refinement(
    ns: tuple[int, ...] = REFINEMENT_NS,
    *,
    n_grid: int = 400,
    n_samples: int = POSTERIOR_SAMPLES,
    verbose: bool = True,
) -> RefinementResult:
    """Compute naive and Bessel posteriors at each resolution in ``ns``.

    This is the single (expensive) source of truth shared by the static F4
    figure and the interactive JSON bundle.
    """
    np.random.seed(0)  # posterior.sample() draws from the global RNG; pin it
    model_space = make_model_space()
    forward = make_forward(model_space)
    m_bar = true_model(model_space)
    data = make_data(forward, m_bar)
    bessel_covariance = make_bessel_covariance(model_space)
    x = plot_grid(n_grid)
    true_vals = np.asarray(m_bar.evaluate(x), dtype=float)
    naive: dict[int, PosteriorCurves] = {}
    bessel: dict[int, PosteriorCurves] = {}
    for n in ns:
        box = hat_coeff_space(n)
        naive[n] = posterior_curves(
            forward, data, box, discrete_prior("naive", box), x, n_samples=n_samples
        )
        bessel[n] = posterior_curves(
            forward, data, box,
            discrete_prior("bessel", box, bessel_covariance=bessel_covariance),
            x, n_samples=n_samples,
        )
        if verbose:
            print(
                f"  N={n:>3}: naive max-std={naive[n].std.max():.3f}"
                f"  bessel max-std={bessel[n].std.max():.3f}",
                flush=True,
            )
    return RefinementResult(
        x=x, true_vals=true_vals, ns=tuple(ns), naive=naive, bessel=bessel, data=data,
    )


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def output_dir() -> Path:
    """``<repo>/media/research/think-first`` (created if missing)."""
    repo_root = Path(__file__).resolve().parents[2]
    out = repo_root / "media" / "research" / "think-first"
    out.mkdir(parents=True, exist_ok=True)
    return out


def plot_grid(n: int = 1000) -> np.ndarray:
    """Dense evaluation grid over the domain for smooth curves."""
    return np.linspace(DOMAIN[0], DOMAIN[1], n)


if __name__ == "__main__":
    M = make_model_space()
    G = make_forward(M)
    data = make_data(G, true_model(M))
    print(f"N_d={N_D}  noise_std={data.noise_std:.4e}")
    for kind in ("hat",):
        disc = discretise(G, kind, 30)
        a_naive = least_norm_coefficients(disc.naive_forward, data)
        a_correct = least_norm_coefficients(disc.correct_forward, data)
        offdiag = float(np.max(np.abs(disc.gram - np.diag(np.diag(disc.gram)))))
        print(
            f"{kind:>3}: max|naive-correct|={np.max(np.abs(a_naive - a_correct)):.3e}"
            f"  gram_offdiag={offdiag:.3e}"
        )
