from abc import ABC, abstractmethod
from itertools import chain


class BaseMetric(ABC):
    @abstractmethod
    def metric(self, source, dest):
        pass

    def best_metric(self, source, dests):
        return max(chain((0,), (self.metric(source, dest) for dest in dests)))


class BaseScorer(ABC):
    @abstractmethod
    def score(self, model, submissions):
        pass
