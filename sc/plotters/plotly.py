import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
import plotly.offline as py
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import Isomap, LocallyLinearEmbedding as LLE, MDS, TSNE

from sc.utils import matplotlib_to_plotly

__all__ = ["PlotlyPlotter"]


class PlotlyPlotter:
    def __init__(self, method="pca", n_dim=2, n_neighbors=5, solver="dense", early_exaggeration=4.):
        self.method = method
        self.n_dim = n_dim
        self.n_neighbors = n_neighbors
        self.solver = solver
        self.early_exaggeration = early_exaggeration

    def _choose_tranformer(self):
        if self.method == "pca":
            return PCA(n_components=self.n_dim)
        elif self.method == "lda":
            return LDA(n_components=self.n_dim, solver=self.solver, shrinkage="auto")
        elif self.method == "imap":
            transformer = Isomap(n_neighbors=n_neighbors, n_components=n_dim).fit_transform(X)
        elif self.method == "lle":
            transformer = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                              eigen_solver=eigen_solver).fit_transform(X)
        elif self.method == "mlle":
            transformer = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                              method="modified", eigen_solver=eigen_solver).fit_transform(X)
        elif self.method == "heig":
            transformer = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                              method="hessian", eigen_solver=eigen_solver).fit_transform(X)
        elif self.method == "ltsa":
            return LLE(n_neighbors=self.n_neighbors, n_components=self.n_dim,
                              method="ltsa", eigen_solver=eigen_solver).fit_transform(X)
        elif self.method == "mds":
            return MDS(n_components=self.n_dim)
        elif self.method == "tsne":
            return TSNE(n_components=self.n_dim, early_exaggeration=self.early_exaggeration)
        else:
            raise ValueError("Such method is't supported yet")

    def plot(self, X, y, *, code=None, correct=None, n_neighbors=5, eigen_solver="dense",
             scaling=None, centres=None, centroids=None, title=None, path="plots/temp_plot.html"):
        if method == "pca":
            reduced_X = PCA(n_components=n_dim).fit_transform(X)
        elif method == "lda":
            reduced_X = LDA(n_components=n_dim, solver="eigen", shrinkage="auto").fit_transform(X, y)
        elif method == "imap":
            reduced_X = Isomap(n_neighbors=n_neighbors, n_components=n_dim).fit_transform(X)
        elif method == "lle":
            reduced_X = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                            eigen_solver=eigen_solver).fit_transform(X)
        elif method == "mlle":
            reduced_X = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                            method="modified", eigen_solver=eigen_solver).fit_transform(X)
        elif method == "heig":
            reduced_X = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                            method="hessian", eigen_solver=eigen_solver).fit_transform(X)
        elif method == "ltsa":
            reduced_X = LLE(n_neighbors=n_neighbors, n_components=n_dim,
                            method="ltsa", eigen_solver=eigen_solver).fit_transform(X)
        elif method == "mds":
            reduced_X = MDS(n_components=n_dim).fit_transform(X)
        elif method == "tsne":
            reduced_X = TSNE(n_components=n_dim, early_exaggeration=1.).fit_transform(X)
        else:
            raise ValueError("Such method is't supported yet")

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

        if n_dim == 2:
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
                color=correct,
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
            if correct is not None:
                layout["updatemenus"] = updatemenus
        elif n_dim == 3:
            # TODO: implement
            raise ValueError("Such dim is't supported yet")
        else:
            raise ValueError("Such dim is't supported yet")

        fig = dict(
            data=data,
            layout=layout
        )
        py.plot(fig, filename=path)
