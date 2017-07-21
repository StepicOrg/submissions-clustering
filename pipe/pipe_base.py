from abc import ABC, abstractmethod
from functools import wraps

from bunch import Bunch
from more_itertools import flatten
from tqdm import tqdm


class Pipe:
    def __init__(self, initer):
        self.state = Bunch()
        self.gen = initer.init(self.state)

    def transform(self, transformer):
        self.gen = transformer.transform(self.gen, self.state)
        return self

    def terminate(self, terminater):
        gen = iter(tqdm(self.gen))
        return terminater.terminate(gen, self.state)


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


def LinPoint(transformer_cls):
    old_transform = transformer_cls.transform

    @wraps(transformer_cls.transform)
    def new_transform(self, gen, state):
        gen = (elem for elem in list(gen))
        return old_transform(gen, state)

    transformer_cls.transform = new_transform
    return transformer_cls


class Terminater(ABC):
    @abstractmethod
    def terminate(self, gen, state):
        pass
