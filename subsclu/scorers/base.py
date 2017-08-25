"""Module for stuff related with score bases."""

from abc import ABC, abstractmethod
from itertools import chain

__all__ = ["Metric", "Scorer"]


class Metric(ABC):
    """Base metric class for metric."""

    @abstractmethod
    def metric(self, source, dest):
        """Calculate distance between source and dest."""
        pass

    def best_metric(self, source, dests):
        """Calculate max distance between source and dests."""
        return max(chain((0,), (self.metric(source, dest) for dest in dests)))


class Scorer(ABC):
    """Base scorer class for score."""

    @abstractmethod
    def score(self, model, submissions, **kwargs):
        """Calculate score of how good model perform on given submissions."""
        pass

    @staticmethod
    def outof(*args, **kwargs):
        """See :func:`subsclu.scorers.spec.scorer_from_spec`."""
        from subsclu.scorers.spec import scorer_from_spec
        return scorer_from_spec(*args, **kwargs)
