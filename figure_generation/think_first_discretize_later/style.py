"""Shared Matplotlib styling with a seaborn mako colorscheme.

Figures are rendered with a transparent background and light foreground colours
so they sit cleanly on the site's dark (#2E3135) panels. Importing this module
selects the headless ``Agg`` backend.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (after backend selection)
import seaborn as sns  # noqa: E402

# Build the mako colormap once at import time.
_MAKO = sns.color_palette("mako", as_cmap=True)
_MAKO_COLORS = sns.color_palette("mako", 10)

# Rendering mode: "space" (default) targets the dark site palette,
# "earth" (FIG_MODE=earth) targets the light/earthy palette. Earth
# variants are saved with an "_earth" filename suffix by save().
MODE = os.environ.get("FIG_MODE", "space").strip().lower()
if MODE not in ("space", "earth"):
    MODE = "space"

if MODE == "space":
    # Colours chosen to read against the site's dark background.
    PALETTE = {
        "true": "#f4a259",      # warm amber  - the true model
        "naive": "#ef6f6c",     # coral red   - the naive (transpose) result
        "correct": "#74c69d",   # green       - the geometry-correct result
        "kernel": "#6791BE",    # site blue   - sensitivity kernels
        "data": "#9ec5fe",      # light blue  - data points
        "accent": "#6791BE",    # site accent
        "muted": "#8b97a7",     # muted grey  - secondary lines / zero mean
        "mako": _MAKO,          # seaborn mako colormap for imshow / heatmaps
        "mako_dark": _MAKO_COLORS[7],   # light-mid mako - primary curves (visible on dark bg)
        "mako_mid": _MAKO_COLORS[8],    # light mako - secondary curves
        "mako_light": _MAKO_COLORS[9],  # pale mako - tertiary / fills
        "mako_pale": _MAKO_COLORS[9],   # palest mako - backgrounds / bands
    }
    _FG = "#dce6f5"   # light foreground for text/ticks
    _SPINE = "#5a6675"
else:
    # Earth mode: same semantic roles, deepened to read on the cream
    # ground (#EDE9DD) of the site's earth palette.
    PALETTE = {
        "true": "#B0741B",      # deep ochre   - the true model
        "naive": "#C24E44",     # brick red    - the naive (transpose) result
        "correct": "#3E7D5E",   # forest green - the geometry-correct result
        "kernel": "#5C6D33",    # moss (site earth accent) - sensitivity kernels
        "data": "#46628F",      # steel blue   - data points
        "accent": "#5C6D33",    # site earth accent
        "muted": "#8A8268",     # warm grey    - secondary lines / zero mean
        "mako": _MAKO,          # mako still reads on light ground
        "mako_dark": _MAKO_COLORS[2],   # dark mako - primary curves (visible on light bg)
        "mako_mid": _MAKO_COLORS[4],    # mid mako - secondary curves
        "mako_light": _MAKO_COLORS[5],  # lighter mako - tertiary / fills
        "mako_pale": _MAKO_COLORS[6],   # palest usable mako on cream
    }
    _FG = "#3A3627"   # dark olive ink for text/ticks
    _SPINE = "#8F8768"

FG = _FG   # public alias for figure scripts


def apply_style() -> None:
    """Set rcParams for transparent, dark-friendly, web-embeddable figures."""
    sns.set_theme(style="dark", palette="mako")
    plt.rcParams.update(
        {
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "savefig.facecolor": "none",
            "savefig.transparent": True,
            "text.color": _FG,
            "axes.labelcolor": _FG,
            "axes.edgecolor": _SPINE,
            "xtick.color": _FG,
            "ytick.color": _FG,
            "axes.titlecolor": _FG,
            "grid.color": _SPINE,
            "grid.alpha": 0.3,
            "grid.linestyle": ":",
            "axes.grid": True,
            "font.size": 13,
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "legend.fontsize": 12,
            "legend.framealpha": 0.0,
            "lines.linewidth": 2.2,
            "svg.fonttype": "none",
            "figure.dpi": 150,
            "image.cmap": "mako",
        }
    )


def mako_n(n: int) -> list:
    """Return ``n`` colours sampled evenly from the full mako palette.

    Warning: the darkest colours in this range will be nearly invisible on
    the site's dark background. Use :func:`mako_light_n` for line plots
    where every curve must be visible.
    """
    return sns.color_palette("mako", n)


def mako_light_n(n: int, start: float = 0.3) -> list:
    """Return ``n`` colours sampled from the lighter portion of mako.

    Skips the darkest ``start`` fraction of the palette so that every
    returned colour is visible on the dark website background. Use this
    for line plots where all curves need to be distinguishable.
    """
    full = sns.color_palette("mako", int(n / (1.0 - start)) + 2)
    if MODE == "earth":
        # on the light ground the LIGHT end is the invisible one -
        # sample from the darker portion instead
        return full[:n]
    return full[int(len(full) * start):][:n]


def save(fig: "plt.Figure", name: str, out_dir: Path) -> None:
    """Save ``fig`` as both transparent PNG and SVG under ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_earth" if MODE == "earth" else ""
    fig.savefig(out_dir / f"{name}{suffix}.png", dpi=200, bbox_inches="tight", transparent=True)
    fig.savefig(out_dir / f"{name}{suffix}.svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
