class SanitizerMixin:
    def fit_sanitize(self, X, **fit_params):
        return self.fit(X, **fit_params).sanitize(X)
