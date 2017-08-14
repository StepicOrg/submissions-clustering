import numpy as np
from sklearn.base import BaseEstimator

from sc import languages
from sc.pipe.bases import SanitizerMixin
from sc.primitives import Tree, DefaultIntBijection

__all__ = ["SimplePreprocessor"]


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    def __init__(self, language, method, *, filter_correct=True, add_unk=True, unk_str="<UNK>"):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.add_unk = add_unk
        self.unk_str = unk_str

        self._encoding = None

    def fit(self, X):
        return self

    def _encode(self, struct):
        if isinstance(struct, list):
            return [self._encoding[elem] for elem in struct]
        elif isinstance(struct, Tree):
            return struct.map(self._encoding)
        else:
            raise ValueError("No such struct supported yet")

    def sanitize(self, X):
        language = languages.from_spec(self.language)
        method = language[self.method]
        self._encoding = DefaultIntBijection(zero_value=self.unk_str if self.add_unk else None)
        ci, s = [], []
        for i, x in enumerate(X):
            if not self.filter_correct or language.check(x):
                ci.append(i)
                s.append(self._encode(method(x)))
        return np.array(ci), s
