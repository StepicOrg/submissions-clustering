from subsclu.exceptions import PipeCompoundError
from subsclu.pipe.bases import BaseEstimator, SanitizerMixin
from subsclu.primitives import Tree, DefaultIntBijection

__all__ = ["StupidPreprocessor", "SimplePreprocessor"]


class StupidPreprocessor(BaseEstimator, SanitizerMixin):
    def fit(self, codes):
        return self

    def sanitize(self, codes):
        return codes


_STRUCTS = (
    (list, [0], lambda l, e: [e[elem] for elem in l]),  # list
    (Tree, Tree(0), lambda t, e: t.map(e))  # Tree
)

_VALID_STRUCTS = tuple(struct for struct, _, _ in _STRUCTS)


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    UNK_STR = "<UNK>"

    def _make_encoding(self):
        return DefaultIntBijection(zero_value=self.UNK_STR if self.add_unk else None)

    def __init__(self, method, add_unk=True):
        self.method = method
        self.add_unk = add_unk

        self._encoding = self._make_encoding()

    def _encode(self, struct):
        for Struct, dummy, encode in _STRUCTS:
            if isinstance(struct, Struct):
                if len(struct):
                    return encode(struct, self._encoding)
                else:
                    return dummy
        raise PipeCompoundError("struct must be of the {}".format(_VALID_STRUCTS))

    def fit(self, codes):
        for code in codes:
            self._encode(self.method(code))
        return self

    def sanitize(self, codes):
        return [self._encode(self.method(code)) for code in codes]

    def fit_sanitize(self, codes, **fit_params):
        """For the sake of speed-up."""
        return self.sanitize(codes)
