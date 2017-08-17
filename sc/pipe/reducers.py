from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE

__all__ = ["PCA", "TruncatedSVD", "TSNE", "reducer_from_spec"]

VALID_NAMES = "pca", "lsa", "lsi", "tsne"


def reducer_from_spec(name, n_dim, **kwargs):
    if name == "pca":
        return PCA(n_components=n_dim, **kwargs)
    elif name in ("lsa", "lsi"):
        return TruncatedSVD(n_components=n_dim, **kwargs)
    elif name == "tsne":
        return TSNE(n_components=n_dim, **kwargs)
    else:
        raise ValueError("name must be of the {}".format(VALID_NAMES))
