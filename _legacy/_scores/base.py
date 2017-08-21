from abc import ABC, abstractmethod
from itertools import chain


class BaseMetric(ABC):
    @abstractmethod
    def score(self, source, destination):
        pass

    def best_score(self, source, destinations):
        return max(chain((0,), (self.score(source, destination) for destination in destinations)))
