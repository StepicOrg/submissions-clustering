__all__ = ["SanitizerMixin", "NeighborsMixin"]


class SanitizerMixin:
    def fit_sanitize(self, X, **fit_params):
        return self.fit(X, **fit_params).sanitize(X)


class NeighborsMixin:
    def fit_neighbors(self, X, y, **fit_params):
        return self.fit(X, y, **fit_params).neighbors(X)
