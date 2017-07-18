from abc import ABCMeta, abstractmethod


class Language(metaclass=ABCMeta):
    @abstractmethod
    def check(self, code):
        pass

    @abstractmethod
    def parse(self, code):
        pass

    @abstractmethod
    def process(self, method, code, encoding):
        pass
