from subsclu import languages
from subsclu.pipe.bases import BaseEstimator, SanitizerMixin
from subsclu.primitives import Tree, DefaultIntBijection

__all__ = ["StupidPreprocessor", "SimplePreprocessor"]


class StupidPreprocessor(BaseEstimator, SanitizerMixin):
    def fit(self, codes):
        return self

    def sanitize(self, codes):
        return codes


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    UNK_STR = "<UNK>"
    VALID_STRUCTS = list, Tree

    def _make_encoding(self):
        return DefaultIntBijection(zero_value=self.UNK_STR if self.add_unk else None)

    def __init__(self, language, method, add_unk=True):
        self.language = language
        self.method = method
        self.add_unk = add_unk

        self._encoding = self._make_encoding()

    def _get_method(self, method):
        language = languages.from_spec(self.language)
        return language[method] if method in language else None

    def _encode(self, struct):
        if isinstance(struct, list):
            return [self._encoding[elem] for elem in struct]
        elif isinstance(struct, Tree):
            return struct.map(self._encoding)
        else:
            raise ValueError("struct must be of the {}".format(self.VALID_STRUCTS))

    def fit(self, codes):
        method = self._get_method(self.method)
        for code in codes:
            self._encode(method(code))
        return self

    def sanitize(self, codes):
        method = self._get_method(self.method)
        return [self._encode(method(code)) for code in codes]

    def fit_sanitize(self, codes, **fit_params):
        """For the sake of speed-up."""
        return self.sanitize(codes)
