from collections import Iterator

from .bijection import DefaultIntBijection
from .languages import Python
from .methods import Tokenize


class Preprocessor(Iterator):
    def __init__(self, code_gen, language=Python(), method=Tokenize(), filter_correct=True, add_unk=True):
        self.code_gen = filter(language.check, code_gen) if filter_correct else code_gen
        self.language = language
        self.method = method
        self.encoding = DefaultIntBijection(zero_value="<UNK>" if add_unk else None)

    def __next__(self):
        return self.language.process(self.method, next(self.code_gen), self.encoding)
