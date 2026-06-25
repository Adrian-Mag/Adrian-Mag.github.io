"""Export ``refinement_sweep.json`` for the interactive N-slider panel.

The JSON bundles, for every resolution N, the naive and Bessel posterior mean
and pointwise std curves (plus the true model and a max-std summary). The web
page's slider reads this file and redraws the +/-2 sigma bands client-side - no
Python at runtime.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import problem_setup as ps

DOWNSAMPLE = 2   # keep every 2nd grid point to shrink the payload
ROUND = 4


def _round(array: np.ndarray) -> list[float]:
    return [round(float(v), ROUND) for v in array]


def _pack(curves: "ps.PosteriorCurves") -> dict:
    return {"mean": _round(curves.mean[::DOWNSAMPLE]), "std": _round(curves.std[::DOWNSAMPLE])}


def main() -> None:
    result = ps.compute_refinement()
    x = result.x[::DOWNSAMPLE]
    payload = {
        "x": _round(x),
        "true": _round(result.true_vals[::DOWNSAMPLE]),
        "ns": list(result.ns),
        "naive": {str(n): _pack(result.naive[n]) for n in result.ns},
        "bessel": {str(n): _pack(result.bessel[n]) for n in result.ns},
        "summary": {
            "ns": list(result.ns),
            "naive_rms_std": _round(np.array([np.sqrt(np.mean(result.naive[n].std ** 2)) for n in result.ns])),
            "bessel_rms_std": _round(np.array([np.sqrt(np.mean(result.bessel[n].std ** 2)) for n in result.ns])),
            "naive_max_std": _round(np.array([result.naive[n].std.max() for n in result.ns])),
            "bessel_max_std": _round(np.array([result.bessel[n].std.max() for n in result.ns])),
        },
        "meta": {
            "domain": list(ps.DOMAIN),
            "n_data": ps.N_D,
            "naive_sigma": ps.NAIVE_SIGMA,
            "bessel_amplitude": ps.BESSEL_AMPLITUDE,
            "bessel_k": ps.BESSEL_K,
            "bessel_s": ps.BESSEL_S,
            "posterior_samples": ps.POSTERIOR_SAMPLES,
        },
    }
    out_path = ps.output_dir() / "refinement_sweep.json"
    out_path.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"wrote {out_path}  ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
