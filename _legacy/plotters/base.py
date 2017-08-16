from abc import ABC, abstractmethod

__all__ = []


class BasePlotter(ABC):
    @abstractmethod
    def plot(self, X, y, centers=None, centroids=None,
             codes=None, statuses=None, title=None, path="temp_plot.html"):
        pass
