from more_itertools import flatten, windowed
from sklearn.feature_extraction.text import HashingVectorizer

__all__ = ["Hash"]


class Hash(HashingVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(windowed(x, i) for i in range(left_bound, min(len(x), right_bound)))

        return analyzer
