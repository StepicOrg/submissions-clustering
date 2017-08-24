import os

import numpy as np

from subsclu.utils import dump, gdisk, iter, matrix, read


class A(dump.LoadSaveMixin):
    def __init__(self):
        self.a, self.b = 1, 2


def test_dump():
    object_ = (1, "kek")
    dump.default_save(object_, "object.dump")
    del object_
    object_ = dump.default_load("object.dump")
    assert object_ == (1, "kek"), "restored value should match initial"
    os.remove("object.dump")

    a = A()
    a.save("a.dump")
    del a
    a = A.load("a.dump")
    assert (a.a, a.b) == (1, 2), "restored value should match initial"
    os.remove("a.dump")


def test_gdisk():
    assert isinstance(gdisk.download_file(gdisk.NAMES[0]), str), "path str"


def test_iter():
    assert list(iter.select_at([0, 1, 2], [0, 2])) == [0, 2], "ch"


def test_matrix():
    assert len(matrix.find_centers(
        np.array([[1, 2], [3, 4]]), np.array([0, 1])
    )) == 2, "two labels - two centers"


def test_read():
    assert read.split_into_lists([(1, 2)]) == ([1], [2]), "test list split"
    assert isinstance(
        list(read.from_file("tests/test_utils.py"))[0][0], str
    ), "code str"
