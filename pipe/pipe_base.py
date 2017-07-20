from abc import ABC, abstractmethod

from bunch import Bunch
from more_itertools import flatten


class Pipe:
    def __init__(self, initer):
        self.state = Bunch()
        self.gen = initer.init(self.state)

    def transform(self, transformer):
        self.gen = transformer.transform(self.gen, self.state)
        return self

    def terminate(self, terminater):
        return terminater.terminate(self.gen, self.state)


class Initer(ABC):
    @abstractmethod
    def init(self, state):
        pass


class Transformer(ABC):
    @abstractmethod
    def transform(self, gen, state):
        pass


class Mapper(Transformer):
    @abstractmethod
    def map(self, elem, state):
        pass

    def transform(self, gen, state):
        return (self.map(elem, state) for elem in gen)


class Expander(Transformer):
    @abstractmethod
    def expand(self, elem, state):
        pass

    def transform(self, gen, state):
        return flatten(self.expand(elem, state) for elem in gen)


class Terminater(ABC):
    @abstractmethod
    def terminate(self, gen, state):
        pass
