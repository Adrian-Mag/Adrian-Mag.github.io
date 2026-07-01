"""Shared Matplotlib styling with a seaborn mako colorscheme.

Figures are rendered with a transparent background and light foreground colours
so they sit cleanly on the site's dark (#2E3135) panels. Importing this module
selects the headless ``Agg`` backend.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (after backend selection)
import seaborn as sns  # noqa: E402

# Build the mako colormap once at import time.
_MAKO = sns.color_palette("mako", as_cmap=True)
_MAKO_COLORS = sns.color_palette("mako", 10)

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
    return full[int(len(full) * start):][:n]


def save(fig: "plt.Figure", name: str, out_dir: Path) -> None:
    """Save ``fig`` as both transparent PNG and SVG under ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"{name}.png", dpi=200, bbox_inches="tight", transparent=True)
    fig.savefig(out_dir / f"{name}.svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
