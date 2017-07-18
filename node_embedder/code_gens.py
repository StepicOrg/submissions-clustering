import os
from abc import ABCMeta
from collections import Iterator
from itertools import chain

import pandas as pd


class CodeGen(Iterator, metaclass=ABCMeta):
    pass


class FromCSV(CodeGen):
    def __init__(self, path, column="code", chunk_size=1000000):
        self.path = path
        self.column = column
        self.chunk_size = chunk_size
        self.it = self.read_csv()

    def __next__(self):
        return next(self.it)

    def read_csv(self):
        yield from chain(*pd.read_csv(self.path, usecols=[self.column], squeeze=True, chunksize=self.chunk_size))


class Walk(CodeGen):
    HIDDEN_PREFIX_CHAR = {'.', '_'}

    def __init__(self, path, ext, ignore_hidden=True):
        self.path = path
        self.ext = ext
        self.ignore_hidden = ignore_hidden
        self.it = self.walk()

    def __next__(self):
        return next(self.it)

    def walk(self):
        for dir_path, dir_names, file_names in os.walk(self.path):
            for file_name in file_names:
                if file_name.endswith(self.ext) \
                        and (not self.ignore_hidden or file_name[0] not in self.HIDDEN_PREFIX_CHAR):
                    yield open(os.path.join(dir_path, file_name)).read()
