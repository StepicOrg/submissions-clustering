import os

import pandas as pd


def from_csv(path, column="code", memory_map=False):
    yield from pd.read_csv(path, usecols=[column], squeeze=True, memory_map=memory_map)


def walk(path, ext, ignore_hidden=True, hidden_prefix_char=frozenset({'.', '_'})):
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(ext) and (not ignore_hidden or file_name[0] not in hidden_prefix_char):
                try:
                    yield open(os.path.join(dir_path, file_name)).read()
                except UnicodeDecodeError:
                    continue


def single_file(path):
    yield open(path).read()