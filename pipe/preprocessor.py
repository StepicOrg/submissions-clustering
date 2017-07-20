from .languages import LANGUAGES
from .pipe_base import Transformer
from .primitives import DefaultIntBijection


class Preprocessor(Transformer):
    UNK_STR = "<UNK>"

    def __init__(self, language, method, filter_correct=True, add_unk=True):
        self.language = language
        self.method = method
        self.filter_correct = filter_correct
        self.add_unk = add_unk

    def transform(self, gen, state):
        language = LANGUAGES[self.language]
        check = language["check"]
        method = language[self.method]
        gen = filter(check, gen) if self.filter_correct else gen
        encoding = DefaultIntBijection(zero_value=self.UNK_STR if self.add_unk else None)
        state.encoding = encoding
        return map(lambda x: method(x, encoding), gen)
