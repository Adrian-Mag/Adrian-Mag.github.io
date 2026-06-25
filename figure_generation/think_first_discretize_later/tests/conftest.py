"""Pytest configuration: make the package importable and register markers."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: expensive numerical tests (Bayesian refinement)")
