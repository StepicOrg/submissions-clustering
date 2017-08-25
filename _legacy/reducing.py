VALID_NAMES = "pca", "lsa", "lsi", "tsne"


def from_spec(name, n_dim, **kwargs):
    if name == "pca":
        return PCA(n_components=n_dim, **kwargs)
    elif name in ("lsa", "lsi"):
        return TruncatedSVD(n_components=n_dim, **kwargs)
    elif name == "tsne":
        return TSNE(n_components=n_dim, **kwargs)
    else:
        raise InvalidSpec("name must be of the {}".format(VALID_NAMES))
