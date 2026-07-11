"""Shared Matplotlib styling for SOLA figures.

Reuses the mako colorscheme from the Think First figures for visual
consistency across research pages. Importing this module selects the
headless ``Agg`` backend.

This module re-exports everything from the Think First ``style.py``
so that SOLA figure scripts can simply ``from style import ...``
without worrying about the path.
"""

from __future__ import annotations

import importlib.util
import os
import sys

# Load the think_first style module by file path to avoid a circular
# import (this file is also named "style").
_TF_STYLE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "think_first_discretize_later",
    "style.py",
)
_spec = importlib.util.spec_from_file_location("_tf_style", _TF_STYLE_PATH)
_tf_style = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tf_style)

# Re-export the public API.
PALETTE = _tf_style.PALETTE
MODE = _tf_style.MODE
FG = _tf_style.FG
apply_style = _tf_style.apply_style
mako_n = _tf_style.mako_n
mako_light_n = _tf_style.mako_light_n
save = _tf_style.save
plt = _tf_style.plt
sns = _tf_style.sns
