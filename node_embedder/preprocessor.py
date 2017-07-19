from collections import Iterator

from .primitives import DefaultIntBijection

UNK_STR = "<UNK>"


class Preprocessor(Iterator):
    def __init__(self, code_gen, language, method, filter_correct=True, add_unk=True):
        self._code_gen = filter(language.check, code_gen) if filter_correct else code_gen
        self._language = language
        self.method = method
        self.encoding = DefaultIntBijection(zero_value=UNK_STR if add_unk else None)

    def __next__(self):
        return self._language.process(self.method, next(self._code_gen), self.encoding)
