import numpy as np

__all__ = ["matplotlib_to_plotly"]


def matplotlib_to_plotly(cmap, pl_entries, add_black=False):
    h = 1.0 / (pl_entries - 1)
    pl_colorscale = []
    for k in range(1 if add_black else 0, pl_entries):
        C = list(map(np.uint8, np.array(cmap(k * h)[:3]) * 255))
        pl_colorscale.append([k * h, 'rgb' + str((C[0], C[1], C[2]))])
    if add_black:
        pl_colorscale.insert(0, [.0, "black"])
    return pl_colorscale
