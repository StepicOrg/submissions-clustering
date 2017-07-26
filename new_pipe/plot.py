import plotly.graph_objs as go
import plotly.offline as py
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def plot(X, y, *, method="pca", n_dim=2, code=None, correct=None, centroid_p=None, title=None, path=None):
    if method == "pca":
        X = PCA(n_components=n_dim).fit_transform(X)
    elif method == "lda":
        X = LDA(n_components=n_dim, solver="eigen", shrinkage="auto").fit_transform(X, y)
    else:
        raise ValueError("Such method is't supported yet")

    if n_dim == 2:
        print(y)
        cluster_marker = dict(
            size=20,
            color=y,
            colorscale="Electric",
            cmin=0,
            cmax=y.max(),
            opacity=0.7
        )
        status_marker = dict(
            size=20,
            color=correct.astype(int),
            colorscale=[[0, "#EF233C"], [1, "#20BF55"]],
            opacity=0.8
        )
        trace = go.Scattergl(
            x=X[:, 0],
            y=X[:, 1],
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
            updatemenus=list([
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
        )
    elif n_dim == 3:
        # TODO: implement
        raise ValueError("Such dim is't supported yet")
    else:
        raise ValueError("Such dim is't supported yet")

    fig = dict(
        data=data,
        layout=layout
    )
    py.plot(fig, filename=path or "temp_plot.html")
