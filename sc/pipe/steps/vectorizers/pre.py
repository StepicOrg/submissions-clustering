from more_itertools import flatten, windowed
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer

__all__ = ["BagOfNgrams", "BagOfTrees", "Hasher"]


class BagOfNgrams(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(windowed(x, i) for i in range(left_bound, min(len(x), right_bound) + 1))

        return analyzer


class BagOfTrees(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(x.subtrees(i) for i in range(left_bound, right_bound + 1))

        return analyzer


class Hasher(HashingVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(x):
            return flatten(windowed(x, i) for i in range(left_bound, min(len(x), right_bound)))

        return analyzer
