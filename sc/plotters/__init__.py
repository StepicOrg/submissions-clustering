from sc.pipe.commons import reducers
from .plotly import *

__all__ = plotly.__all__

VALID_NAMES = "plotly2d",


def from_spec(name, **kwargs):
    if name == "plotly2d":
        return Plotly2DPlotter(reducer=reducers.from_spec("pca", 2), **kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
