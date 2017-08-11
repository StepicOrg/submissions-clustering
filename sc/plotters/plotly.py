import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py

from sc.utils import matplotlib_to_plotly

__all__ = ["Plotly2DPlotter"]


class Plotly2DPlotter:
    VALID_SCALINGS = "centers", "centroids"

    def __init__(self, reducer, scaling=None):
        self.reducer = reducer
        self.scaling = scaling

    def __calc_centroid_p(self, X, y, centers, centroids):
        if self.scaling is None:
            pass
        elif self.scaling == "centers":
            pass
        elif self.scaling == "centroids":
            pass
        else:
            raise ValueError(f"scaling must be one of the {self.VALID_SCALINGS}")

    def plot(self, X, y, *, code=None, status=None,
             centres=None, centroids=None, title=None, path="plots/temp_plot.html"):
        reduced_X = self.reducer.fit_transform(X, y)

        if scaling is None:
            centroid_p = np.ones(X.shape[0]) * .5
        elif scaling == "auto":
            # TODO: implement
            raise ValueError("Such scaling is't supported yet")
        elif scaling == "centers" and centres is not None:
            centroid_p = np.linalg.norm(X - centres[y], axis=1) ** 2
            max_d = np.zeros(y.max() + 1, dtype=np.float)
            for i, c_p in enumerate(centroid_p):
                max_d[y[i]] = max(max_d[y[i]], c_p)
            centroid_p = 1 - centroid_p / max_d[y]
        elif scaling == "centroids" and centroids is not None:
            # TODO: implement
            raise ValueError("Such scaling is't supported yet")
        else:
            raise ValueError("Such scaling is't supported yet")
        centroid_p[y == -1] = .0

        min_size, max_size = 8, 25
        colorscale = matplotlib_to_plotly(plt.cm.Paired, y.max() + 1, add_black=y.min() == -1)
        cluster_marker = dict(
            size=min_size + centroid_p * (max_size - min_size),
            color=y,
            colorscale=colorscale,
            opacity=0.85,
            line=dict(
                width=0
            )
        )
        status_marker = dict(
            size=15,
            color=status,
            colorscale=[[0, "#EF233C"], [1, "#20BF55"]],
            cmin=0,
            cmax=1,
            opacity=0.8,
            line=dict(
                width=0
            )
        )
        trace = go.Scattergl(
            x=reduced_X[:, 0],
            y=reduced_X[:, 1],
            mode="markers",
            text=code,
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
        if code is not None:
            trace["text"] = code.map(lambda s: s.replace("\n", "<br>"))
        data = [trace]
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
        if status is not None:
            layout["updatemenus"] = updatemenus

        fig = dict(
            data=data,
            layout=layout
        )
        py.plot(fig, filename=path)
