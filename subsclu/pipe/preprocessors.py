import numpy as np

from subsclu import languages
from subsclu.pipe.bases import BaseEstimator, SanitizerMixin
from subsclu.primitives import Tree, DefaultIntBijection

__all__ = ["SimplePreprocessor"]


class SimplePreprocessor(BaseEstimator, SanitizerMixin):
    UNK_STR = "<UNK>"
    VALID_STRUCTS = list, Tree

    def _make_encoding(self):
        return DefaultIntBijection(zero_value=self.UNK_STR if self.add_unk else None)

    def __init__(self, language, method, filter_correct=True, check_method="check",
                 filter_empty=True, add_unk=True):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.check_method = check_method
        self.filter_empty = filter_empty
        self.add_unk = add_unk

        self._encoding = self._make_encoding()

    def _get_methods(self, *methods):
        language = languages.from_spec(self.language)
        return tuple((language[method] if method in language else None) for method in methods)

    def _encode(self, struct):
        if isinstance(struct, list):
            return [self._encoding[elem] for elem in struct]
        elif isinstance(struct, Tree):
            return struct.map(self._encoding)
        else:
            raise ValueError("struct must be of the {}".format(self.VALID_STRUCTS))

    def fit(self, codes):
        method, check = self._get_methods(self.method, self.check_method)
        for code in codes:
            if not self.filter_correct or check(code):
                self._encode(method(code))
        return self

    def sanitize(self, codes):
        method, check = self._get_methods(self.method, self.check_method)
        correct_indicies, structs = [], []
        for ind, code in enumerate(codes):
            if not self.filter_correct or check(code):
                struct = method(code)
                if not self.filter_empty or len(struct):
                    correct_indicies.append(ind)
                    structs.append(self._encode(struct))
        return np.array(correct_indicies), structs
