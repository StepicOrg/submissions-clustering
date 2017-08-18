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