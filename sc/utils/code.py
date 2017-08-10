import os

import pandas as pd

__all__ = ["from_csv_gen", "walk_gen", "single_file_gen", "from_csv"]


def from_csv_gen(path, columns=("code",), nrows=None, memory_map=False):
    yield from pd.read_csv(path, usecols=columns, nrows=nrows, memory_map=memory_map)[columns].itertuples(index=False)


def walk_gen(path, ext, ignore_hidden=True, hidden_prefix_char=frozenset({'.', '_'})):
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(ext) and (not ignore_hidden or file_name[0] not in hidden_prefix_char):
                try:
                    yield open(os.path.join(dir_path, file_name)).read()
                except UnicodeDecodeError:
                    continue


def single_file_gen(path):
    yield open(path).read()


def from_csv(path, nrows=None):
    df = pd.read_csv(path, nrows=nrows)
    return df.code.tolist(), df.status.tolist()
