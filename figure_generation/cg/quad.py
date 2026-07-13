"""Shared 2-D quadratic test problem for the CG figures.

The model problem is J(v) = (1/2)(Av, v) with minimizer at the origin
(f = 0), where A is SPD with condition number ``kappa`` and principal
axes rotated by ``theta_deg``. All figure scripts draw the same
landscape so the reader recognizes it from act to act.
"""

from __future__ import annotations

import numpy as np

from style import MODE

# Figures render transparent and sit directly on the page ground, so
# annotation halos must match the theme ground to look seamless.
GROUND = "#EDE9DD" if MODE == "earth" else "#16191F"
HALO = dict(boxstyle="round,pad=0.3", facecolor=GROUND, edgecolor="none", alpha=0.88)
LEGEND_PATCH = dict(frameon=True, facecolor=GROUND, edgecolor="none", framealpha=0.9)

THETA_DEG = -30.0


def make_A(kappa: float, theta_deg: float = THETA_DEG) -> np.ndarray:
    th = np.deg2rad(theta_deg)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    D = np.diag([kappa, 1.0])
    return R @ D @ R.T


def J(A: np.ndarray, X, Y):
    return 0.5 * (A[0, 0] * X * X + 2 * A[0, 1] * X * Y + A[1, 1] * Y * Y)


def grad(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    return A @ x


def energy_norm(A: np.ndarray, x: np.ndarray) -> float:
    return float(np.sqrt(x @ (A @ x)))


def worst_start(A: np.ndarray, scale: float = 2.2, signs=(1.0, 1.0)) -> np.ndarray:
    """A starting point that makes steepest descent contract at its
    worst-case rate (kappa-1)/(kappa+1): equal error components along the
    extreme eigenvectors, measured in the energy norm."""
    w, V = np.linalg.eigh(A)
    x = signs[0] * V[:, 0] / np.sqrt(w[0]) + signs[1] * V[:, 1] / np.sqrt(w[1])
    return scale * x / np.linalg.norm(x)


def gd_path(A: np.ndarray, x0, tol: float = 1e-10, maxit: int = 800) -> np.ndarray:
    """Steepest descent with exact line search; returns iterates as rows."""
    x = np.array(x0, dtype=float)
    xs = [x.copy()]
    for _ in range(maxit):
        r = -(A @ x)
        rr = r @ r
        if rr < tol * tol:
            break
        alpha = rr / (r @ (A @ r))
        x = x + alpha * r
        xs.append(x.copy())
    return np.array(xs)


def conjugate_path(A: np.ndarray, x0, p0) -> np.ndarray:
    """Two exact line searches along A-conjugate directions, starting
    from an ARBITRARY first direction p0 (not necessarily the residual)."""
    x = np.array(x0, dtype=float)
    p = np.array(p0, dtype=float)
    xs = [x.copy()]
    for _ in range(2):
        r = -(A @ x)
        Ap = A @ p
        alpha = (r @ p) / (p @ Ap)
        x = x + alpha * p
        xs.append(x.copy())
        r_new = -(A @ x)
        beta = -(r_new @ Ap) / (p @ Ap)
        p = r_new + beta * p
    return np.array(xs)


def cg_path(A: np.ndarray, x0, tol: float = 1e-12, maxit: int | None = None) -> np.ndarray:
    x = np.array(x0, dtype=float)
    xs = [x.copy()]
    r = -(A @ x)
    p = r.copy()
    n = maxit if maxit is not None else len(x)
    for _ in range(n):
        rr = r @ r
        if rr < tol * tol:
            break
        Ap = A @ p
        alpha = rr / (p @ Ap)
        x = x + alpha * p
        xs.append(x.copy())
        r = r - alpha * Ap
        beta = (r @ r) / rr
        p = r + beta * p
    return np.array(xs)


def contour_levels(A: np.ndarray, xs_list, n: int = 8):
    """Geometric ladder of J-levels that covers the given paths."""
    jmax = max(J(A, p[:, 0], p[:, 1]).max() for p in xs_list)
    return list(jmax * np.power(0.42, np.arange(n))[::-1])
