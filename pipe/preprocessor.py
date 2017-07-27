from sklearn.base import BaseEstimator, TransformerMixin

from .languages import languages
from .primitives import DefaultIntBijection


def encode(struct, encoding):
    if isinstance(struct, list):
        return [encoding[elem] for elem in struct]
    else:
        return struct.map(encoding)


class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, language, method, filter_correct=True, add_unk=True, unk_str="<UNK>"):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.add_unk = add_unk
        self.unk_str = unk_str

        self.encoding = DefaultIntBijection(zero_value=unk_str if add_unk else None)
        self.correct_ind = []

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        language = languages[self.language]
        nX = []
        for i, x in enumerate(X):
            if not self.filter_correct or (self.filter_correct and language.check(x)):
                self.correct_ind.append(i)
                nX.append(x)
        X = nX
        X = map(language[self.method], X)
        X = map(lambda x: encode(x, self.encoding), X)
        return list(X)
