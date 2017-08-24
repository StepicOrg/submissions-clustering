"""Stuff related to reading data."""

import logging
import os
import sqlite3

import pandas as pd

from subsclu.languages import Language

__all__ = ["split_into_lists", "from_file", "from_walk",
           "from_csv", "from_sl3", "filter_out_invalid"]

logger = logging.getLogger(__name__)


def split_into_lists(iterator):
    """Split iterator of two-tuples into two lists."""
    return tuple(map(list, zip(*iterator)))


def _fix_and_split(iterator):
    iterator = ((str(a), str(b)) for a, b in iterator)
    return split_into_lists(iterator)


def _file_gen(path, status="correct"):
    logger.info("gen code from file %s", path)
    yield open(path).read(), status


def from_file(*args, **kwargs):
    """Read from file."""
    gen = kwargs.pop("gen", True)
    iterator = _file_gen(*args, **kwargs)
    return iterator if gen else _fix_and_split(iterator)


def _walk_gen(path, ext, ignore_hidden=True,
              hidden_prefix_char=frozenset({'.', '_'}), status="correct"):
    logger.info("gen codes from path %s", path)
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(ext) \
                    and (not ignore_hidden
                         or file_name[0] not in hidden_prefix_char):
                try:
                    code = open(os.path.join(dir_path, file_name)).read()
                    yield code, status
                except UnicodeDecodeError:
                    continue


def from_walk(*args, **kwargs):
    """Read from walk."""
    gen = kwargs.pop("gen", True)
    iterator = _walk_gen(*args, **kwargs)
    return iterator if gen else _fix_and_split(iterator)


def _csv_gen(path, columns=("code", "status"), nrows=None, memory_map=False):
    logger.info("gen codes from csv %s", path)
    yield from pd.read_csv(
        path, usecols=columns,
        nrows=nrows, memory_map=memory_map
    ).loc[:, columns].itertuples(index=False)


def from_csv(*args, **kwargs):
    """Read from csv."""
    gen = kwargs.pop("gen", True)
    iterator = _csv_gen(*args, **kwargs)
    return iterator if gen else _fix_and_split(iterator)


def _sl3_gen(path, table="subs", nrows=None):
    logger.info("gen codes from sqlite3 db at %s", path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        query = "SELECT\n" \
                "  code,\n" \
                "  status\n" \
                "FROM {}{};".format(table,
                                    " LIMIT {}".format(nrows) if nrows else "")
        return cursor.execute(query)


def from_sl3(*args, **kwargs):
    """Read subs from sqlite3 db."""
    gen = kwargs.pop("gen", True)
    iterator = _sl3_gen(*args, **kwargs)
    return iterator if gen else _fix_and_split(iterator)


def filter_out_invalid(submissions, language):
    """Filter correct codes."""
    check = Language.outof(language).check
    return ((code, status) for code, status in submissions if check(code))
