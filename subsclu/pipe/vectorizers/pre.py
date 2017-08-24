"""Stuff related to simple counting methods."""

from more_itertools import flatten, windowed
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer

__all__ = ["BagOfNgrams", "BagOfTrees", "Hasher"]


class BagOfNgrams(CountVectorizer):
    """BON method using sklearn."""

    def build_analyzer(self):
        """Build analyzer func for splitting into ngrams."""
        left_bound, right_bound = self.ngram_range

        def analyzer(vec):
            """Analyzer."""
            return flatten(
                windowed(vec, bound)
                for bound in range(left_bound, min(len(vec), right_bound) + 1)
            )

        return analyzer


class BagOfTrees(CountVectorizer):
    """BOW method using sklearn."""

    def build_analyzer(self):
        """Build analyzer func for splitting into subtrees."""
        left_bound, right_bound = self.ngram_range

        def analyzer(tree):
            """Analyzer."""
            return flatten(tree.subtrees(bound)
                           for bound in range(left_bound, right_bound + 1))

        return analyzer


class Hasher(HashingVectorizer):
    """Hashing vectorizer using sklearn."""

    def build_analyzer(self):
        """Build analyzer func for splitting into ngrams."""
        left_bound, right_bound = self.ngram_range

        def analyzer(vec):
            """Analyzer."""
            return flatten(
                windowed(vec, bound)
                for bound in range(left_bound, min(len(vec), right_bound) + 1)
            )

        return analyzer
