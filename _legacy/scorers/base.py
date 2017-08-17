from abc import ABC, abstractmethod

__all__ = []


class BaseScorer(ABC):
    @abstractmethod
    def score(self, src, dst):
        pass
