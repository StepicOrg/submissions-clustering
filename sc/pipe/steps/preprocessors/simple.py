import numpy as np

from sc.languages import language_from_spec
from sc.pipe.bases import BaseEstimator, SanitizerMixin
from sc.primitives import Tree, DefaultIntBijection

__all__ = ["SimplePreprocessor"]


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    UNK_STR = "<UNK>"
    VALID_STRUCTS = list, Tree

    def __make_encoding(self):
        return DefaultIntBijection(zero_value=self.UNK_STR if self.add_unk else None)

    def __init__(self, language, method, filter_correct=True, check_method="check", filter_empty=True, add_unk=True):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.check_method = check_method
        self.filter_empty = filter_empty
        self.add_unk = add_unk

        self.__encoding = self.__make_encoding()

    def __get_language(self):
        return language_from_spec(self.language)

    def __get_method(self, method):
        language = self.__get_language()
        return language[method] if method in language else None

    def __encode(self, struct):
        if isinstance(struct, list):
            return [self.__encoding[elem] for elem in struct]
        elif isinstance(struct, Tree):
            return struct.map(self.__encoding)
        else:
            raise ValueError(f"struct must be of the {self.VALID_STRUCTS}")

    def fit(self, X, y=None):
        method = self.__get_method(self.method)
        check = self.__get_method(self.check_method)
        for x in X:
            if not self.filter_correct or check(x):
                _ = self.__encode(method(x))
        return self

    def sanitize(self, X):
        method = self.__get_method(self.method)
        check = self.__get_method(self.check_method)
        ci, es = [], []
        for i, x in enumerate(X):
            if not self.filter_correct or check(x):
                s = method(x)
                if not self.filter_empty or len(s):
                    ci.append(i)
                    es.append(self.__encode(s))
        return np.array(ci), es
