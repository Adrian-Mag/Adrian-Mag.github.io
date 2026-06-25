"""Numerical checks that pin the page's central claims.

Fast tests assert the geometry result (boxcar naive == correct, hat naive !=
correct, and the corresponding Gram structure). One slow test confirms the
posterior-under-refinement behaviour (naive diverges, Bessel stays bounded).

Run all:            pytest
Skip the slow one:  pytest -m "not slow"
"""

import numpy as np
import pytest

import problem_setup as ps


@pytest.fixture(scope="module")
def problem():
    model_space = ps.make_model_space()
    forward = ps.make_forward(model_space)
    data = ps.make_data(forward, ps.true_model(model_space))
    return model_space, forward, data


def test_boxcar_gram_is_diagonal(problem):
    _, forward, _ = problem
    disc = ps.discretise(forward, "box", 30)
    off_diagonal = np.max(np.abs(disc.gram - np.diag(np.diag(disc.gram))))
    assert off_diagonal < 1e-9


def test_hat_gram_is_coupled(problem):
    _, forward, _ = problem
    disc = ps.discretise(forward, "hat", 30)
    off_diagonal = np.max(np.abs(disc.gram - np.diag(np.diag(disc.gram))))
    assert off_diagonal > 1e-3


def test_boxcar_naive_equals_correct(problem):
    """The trap: an orthogonal boxcar basis hides the adjoint bug."""
    _, forward, data = problem
    disc = ps.discretise(forward, "box", 30)
    a_naive = ps.least_norm_coefficients(disc.naive_forward, data)
    a_correct = ps.least_norm_coefficients(disc.correct_forward, data)
    np.testing.assert_allclose(a_naive, a_correct, atol=5e-3)


def test_hat_naive_differs_from_correct(problem):
    """The reveal: a non-orthogonal hat basis exposes the adjoint bug."""
    _, forward, data = problem
    disc = ps.discretise(forward, "hat", 30)
    a_naive = ps.least_norm_coefficients(disc.naive_forward, data)
    a_correct = ps.least_norm_coefficients(disc.correct_forward, data)
    assert np.max(np.abs(a_naive - a_correct)) > 0.05


@pytest.mark.slow
def test_refinement_naive_diverges_bessel_bounded():
    """Naive sigma^2 I posterior std grows with N; Bessel stays bounded."""
    result = ps.compute_refinement(ns=(10, 30), n_samples=20, verbose=False)
    naive_10 = result.naive[10].std.max()
    naive_30 = result.naive[30].std.max()
    bessel_10 = result.bessel[10].std.max()
    bessel_30 = result.bessel[30].std.max()
    assert naive_30 > 1.2 * naive_10        # naive grows with refinement
    assert max(bessel_10, bessel_30) < 0.5  # bessel stays bounded
    assert naive_30 > 5 * bessel_30         # naive >> bessel at fine resolution
