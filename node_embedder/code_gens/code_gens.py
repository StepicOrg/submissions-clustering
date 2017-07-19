import os
from abc import ABCMeta
from collections import Iterator
from itertools import chain

import pandas as pd


class CodeGen(Iterator, metaclass=ABCMeta):
    pass


class FromCSV(CodeGen):
    def __init__(self, path, column="code"):
        self.path = path
        self.column = column
        self._it = self._read_csv()

    def __next__(self):
        return next(self._it)

    def _read_csv(self):
        yield from chain(*pd.read_csv(self.path, usecols=[self.column], squeeze=True))


class Walk(CodeGen):
    HIDDEN_PREFIX_CHAR = {'.', '_'}

    def __init__(self, path, ext, ignore_hidden=True):
        self.path = path
        self.ext = ext
        self.ignore_hidden = ignore_hidden
        self._it = self._walk()

    def __next__(self):
        return next(self._it)

    def _walk(self):
        for dir_path, dir_names, file_names in os.walk(self.path):
            for file_name in file_names:
                if file_name.endswith(self.ext) \
                        and (not self.ignore_hidden or file_name[0] not in self.HIDDEN_PREFIX_CHAR):
                    yield open(os.path.join(dir_path, file_name)).read()
