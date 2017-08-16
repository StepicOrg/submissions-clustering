from sc.pipe.commons.reducers import reducer_from_spec
from .plotly import *

__all__ = ["plotter_from_spec"]

VALID_NAMES = "plotly",


def plotter_from_spec(name, **kwargs):
    if name == "plotly":
        return Plotly2DPlotter(reducer=reducer_from_spec("pca", 2), **kwargs)
    else:
        raise ValueError(f"name must be of the {VALID_NAMES}")
