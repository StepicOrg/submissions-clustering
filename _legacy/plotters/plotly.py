import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py
from scipy.ndimage import maximum

from sc.utils.plot import colorscale_from_mpl
from .base import BasePlotter

__all__ = ["Plotly2DPlotter"]


class Plotly2DPlotter(BasePlotter):
    VALID_SCALINGS = "centers", "centroids"

    def __init__(self, reducer, scaling=None, size_range=(8, 25)):
        self.reducer = reducer
        self.scaling = scaling
        self.size_range = size_range

    def __calc_centroid_p(self, X, y, centers, centroids):
        if self.scaling is None:
            centroid_p = np.full(X.shape[0], .5)
            centroid_p[y == -1] = .0
            return centroid_p
        elif self.scaling == "centers":
            dists = np.linalg.norm(X - centers[y], axis=1) ** 2
            centroid_p = 1 - dists / maximum(dists, y)[y]
            centroid_p[y == -1] = .0
            return centroid_p
        elif self.scaling == "centroids":
            # TODO: implement
            pass
        else:
            raise ValueError(f"scaling must be one of the {self.VALID_SCALINGS}")

    def __make_cluster_marker(self, y, centroid_p):
        min_size, max_size = self.size_range
        colorscale = colorscale_from_mpl(plt.cm.Paired, y.max() + 1, add_black=y.min() == -1)
        return dict(
            size=min_size + centroid_p * (max_size - min_size),
            color=y,
            colorscale=colorscale,
            opacity=0.85,
            line=dict(
                width=0
            )
        )

    def __make_status_marker(self, statuses):
        return dict(
            size=15,
            color=(statuses == "correct").astype(float),
            colorscale=[[0, "#EF233C"], [1, "#20BF55"]],
            cmin=0,
            cmax=1,
            opacity=0.8,
            line=dict(
                width=0
            )
        )

    def __make_data(self, reduced_X, cluster_marker, codes):
        trace = go.Scattergl(
            x=reduced_X[:, 0],
            y=reduced_X[:, 1],
            mode="markers",
            text=codes,
            marker=cluster_marker,
            name="trace2d",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor="#272822",
                bordercolor="#272822",
                font=dict(
                    size=14,
                    color="#F8F8F2"
                )
            )
        )
        if codes is not None:
            trace["text"] = codes.map(lambda s: s.replace("\n", "<br>"))
        return [trace]

    def __make_layout(self, cluster_marker, status_marker, statuses, title):
        layout = dict(
            title=title or "Clustering",
            titlefont=dict(
                size=25
            ),
            xaxis=dict(
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                zeroline=False,
                showticklabels=False
            ),
        )
        updatemenus = list([
            dict(
                buttons=list([
                    dict(
                        args=['marker', [cluster_marker]],
                        label='Clusters',
                        method='restyle'
                    ),
                    dict(
                        args=['marker', [status_marker]],
                        label='Status',
                        method='restyle'
                    )
                ]),
                direction='left',
                pad={'r': 10, 't': 10},
                showactive=False,
                type='buttons',
                x=0.1,
                xanchor='left',
                y=1.1,
                yanchor='top'
            )
        ])
        if statuses is not None:
            layout["updatemenus"] = updatemenus
        return layout

    def plot(self, X, y, centers=None, centroids=None,
             codes=None, statuses=None, title=None, path="temp_plot.html"):
        reduced_X = self.reducer.fit_transform(X, y)
        centroid_p = self.__calc_centroid_p(X, y, centers, centroids)
        cluster_marker = self.__make_cluster_marker(y, centroid_p)
        status_marker = self.__make_status_marker(statuses)
        data = self.__make_data(reduced_X, cluster_marker, codes)
        layout = self.__make_layout(cluster_marker, status_marker, statuses, title)
        fig = dict(data=data, layout=layout)
        py.plot(fig, filename=path)
