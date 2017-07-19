from abc import abstractmethod, ABC


class Language(ABC):
    @abstractmethod
    def check(self, code):
        pass

    @abstractmethod
    def process(self, method, code, encoding):
        pass
