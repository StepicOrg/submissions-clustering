from abc import ABC, abstractmethod
from itertools import chain

__all__ = []


class BaseScorer(ABC):
    @abstractmethod
    def score(self, src, dst):
        pass

    def best_score(self, src, dst_it):
        return max(chain((0,), (self.score(src, dst) for dst in dst_it)))
