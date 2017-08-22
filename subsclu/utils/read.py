import logging
import os
import sqlite3

import pandas as pd

from subsclu import languages

logger = logging.getLogger(__name__)


def split_into_lists(it):
    return tuple(map(list, zip(*it)))


def _fix_and_split(it):
    it = ((str(a), str(b)) for a, b in it)
    return split_into_lists(it)


def _file_gen(path, status="correct"):
    logger.info("gen code from file {}".format(path))
    yield open(path).read(), status


def from_file(*args, **kwargs):
    gen = kwargs.pop("gen", True)
    it = _file_gen(*args, **kwargs)
    return it if gen else _fix_and_split(it)


def _walk_gen(path, ext, ignore_hidden=True, hidden_prefix_char=frozenset({'.', '_'}),
              status="correct"):
    logger.info("gen codes from path {}".format(path))
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(ext) \
                    and (not ignore_hidden or file_name[0] not in hidden_prefix_char):
                try:
                    yield open(os.path.join(dir_path, file_name)).read(), status
                except UnicodeDecodeError:
                    continue


def from_walk(*args, **kwargs):
    gen = kwargs.pop("gen", True)
    it = _walk_gen(*args, **kwargs)
    return it if gen else _fix_and_split(it)


def _csv_gen(path, columns=("code", "status"), nrows=None, memory_map=False):
    logger.info("gen codes from csv {}".format(path))
    yield from pd.read_csv(path, usecols=columns, nrows=nrows, memory_map=memory_map) \
                   .loc[:, columns].itertuples(index=False)


def from_csv(*args, **kwargs):
    gen = kwargs.pop("gen", True)
    it = _csv_gen(*args, **kwargs)
    return it if gen else _fix_and_split(it)


def _sl3_gen(path, table="subs", nrows=None):
    logger.info("gen codes from sqlite3 db at {}".format(path))
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        q = "SELECT\n" \
            "  code,\n" \
            "  status\n" \
            "FROM {}{};".format(table, " LIMIT {}".format(nrows) if nrows else "")
        return c.execute(q)


def from_sl3(*args, **kwargs):
    gen = kwargs.pop("gen", True)
    it = _sl3_gen(*args, **kwargs)
    return it if gen else _fix_and_split(it)


def filter_out_invalid(submissions, language):
    check = languages.from_spec(language).check
    return ((code, status) for code, status in submissions if check(code))
