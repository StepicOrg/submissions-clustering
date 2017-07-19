from abc import ABCMeta
from collections import Iterator

from ..methods import *


class Cooker(Iterator, metaclass=ABCMeta):
    pass


BAG_OF_WORDS_SUPPORTED_METHODS = Tokenize,


class BagOfWords(Cooker):
    def __init__(self, preprocessor):
        assert isinstance(preprocessor.method, BAG_OF_WORDS_SUPPORTED_METHODS)
        self.encoding = preprocessor.encoding

    def __next__(self):
        pass


def dump(cooker, path):
    pass


def undump(path):
    pass
