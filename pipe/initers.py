import os

import pandas as pd

from .pipe_base import Initer


class FromCSV(Initer):
    def __init__(self, path, column="code", memory_map=False):
        self.path = path
        self.column = column
        self.memory_map = memory_map

    def init(self, state):
        yield from pd.read_csv(self.path, usecols=[self.column], squeeze=True, memory_map=self.memory_map)


class Walk(Initer):
    HIDDEN_PREFIX_CHAR = {'.', '_'}

    def __init__(self, path, ext, ignore_hidden=True):
        self.path = path
        self.ext = ext
        self.ignore_hidden = ignore_hidden

    def init(self, state):
        for dir_path, dir_names, file_names in os.walk(self.path):
            for file_name in file_names:
                if file_name.endswith(self.ext) \
                        and (not self.ignore_hidden or file_name[0] not in self.HIDDEN_PREFIX_CHAR):
                    try:
                        yield open(os.path.join(dir_path, file_name)).read()
                    except UnicodeDecodeError:
                        continue


class SingleFile(Initer):
    def __init__(self, path):
        self.path = path

    def init(self, state):
        yield open(self.path).read()
