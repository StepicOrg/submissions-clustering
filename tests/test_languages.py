import sys

import pytest

from subsclu.exceptions import InvalidSpec
from subsclu.languages import Language, Python


def test_language():
    def f():
        return 0

    language = Language(
        methods={"a": f}
    )

    assert language.a() == f() == 0, "invoking same funcs"
    assert language["a"]() == f() == 0, "invoking same funcs"
    assert language.a is f, "same funcs have same ids"
    assert language.attrs == ["a"], "list of methods has only 'a'"


def test_outof():
    assert isinstance(
        Language.outof("python"), Python
    ), "should not raise an error, there is such language"
    with pytest.raises(
            InvalidSpec,
            message="should not raise an error, there is not such language"):
        _ = Language.outof("nolng")


def test_python():
    python = Python()
    assert python.check("a=3"), "example of correct py code"
    assert not python.check("|*|"), "example of incorrect py code"
    assert "tokenize" in python, "tokenize should be supported"
    assert "astize" in python, "astize should be supported"
    assert python.version == sys.version_info[:3], "version match"
