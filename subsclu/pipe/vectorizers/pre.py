from more_itertools import flatten, windowed
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer

__all__ = ["BagOfNgrams", "BagOfTrees", "Hasher"]


class BagOfNgrams(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(vec):
            return flatten(windowed(vec, bound)
                           for bound in range(left_bound, min(len(vec), right_bound) + 1))

        return analyzer


class BagOfTrees(CountVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(tree):
            return flatten(tree.subtrees(bound)
                           for bound in range(left_bound, right_bound + 1))

        return analyzer


class Hasher(HashingVectorizer):
    def build_analyzer(self):
        left_bound, right_bound = self.ngram_range

        def analyzer(vec):
            return flatten(windowed(vec, bound)
                           for bound in range(left_bound, min(len(vec), right_bound) + 1))

        return analyzer
