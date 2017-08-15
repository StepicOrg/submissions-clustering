import numpy as np

from sc.pipe.bases import BaseEstimator, SanitizerMixin
from sc.primitives import Tree, DefaultIntBijection

__all__ = ["SimplePreprocessor"]


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    def __init__(self, language, method, filter_correct=True, check_method="check", add_unk=True, unk_str="<UNK>"):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.check_method = check_method
        self.add_unk = add_unk
        self.unk_str = unk_str

        self.__encoding = None

    def fit(self, X):
        return self

    VALID_STRUCTS = list, Tree

    def __encode(self, struct):
        if isinstance(struct, list):
            return [self.__encoding[elem] for elem in struct]
        elif isinstance(struct, Tree):
            return struct.map(self.__encoding)
        else:
            raise ValueError(f"struct must be of the {self.VALID_STRUCTS}")

    def sanitize(self, X):
        method = self.language[self.method]
        check = self.language[self.check_method] if self.check_method in self.language else None
        self.__encoding = DefaultIntBijection(zero_value=self.unk_str if self.add_unk else None)
        ci, s = [], []
        for i, x in enumerate(X):
            if not self.filter_correct or check(x):
                ci.append(i)
                s.append(self.__encode(method(x)))
        return np.array(ci), s
