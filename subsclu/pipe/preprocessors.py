"""Implementation of preprocessor step."""

import numpy as np

from subsclu.exceptions import InvalidPipeCompound
from subsclu.pipe.bases import BaseEstimator, SanitizerMixin
from subsclu.primitives import Tree, DefaultIntBijection

__all__ = ["StupidPreprocessor", "CodePreprocessor"]


class StupidPreprocessor(BaseEstimator, SanitizerMixin):
    """Simple preprocessor, doing nothing."""

    def fit(self, codes):
        # pylint: disable=unused-argument
        """Doint nothing."""
        return self

    def sanitize(self, codes):
        # pylint: disable=no-self-use
        """Doing nothing, return codes back."""
        return codes


_STRUCTS_INFO = (
    (list, [0], lambda l, e: [e[elem] for elem in l]),  # list
    (Tree, Tree(0), lambda t, e: t.map(e))  # Tree
)

_VALID_STRUCTS = tuple(struct for struct, _, _ in _STRUCTS_INFO)


class CodePreprocessor(BaseEstimator, SanitizerMixin):
    """Code preprocessor."""

    UNK_STR = "<UNK>"
    """Object to map 0 to."""

    def _make_encoding(self):
        return DefaultIntBijection(
            zero_value=self.UNK_STR if self.add_unk else None
        )

    def __init__(self, method, check=None, add_unk=True):
        """Make preprocessor with method.

        Args:
            method: Method to use.
            check: Check func.
            add_unk (bool): True if add zero unk value.
        """
        self.method = method
        self.check = check or (lambda _: True)
        self.add_unk = add_unk

        self._encoding = self._make_encoding()

    def _encode(self, struct):
        for class_, dummy, encode in _STRUCTS_INFO:
            if isinstance(struct, class_):
                if struct:
                    return encode(struct, self._encoding)
                return dummy
        raise InvalidPipeCompound("struct must be of the {}"
                                  .format(_VALID_STRUCTS))

    def fit(self, codes):
        """Fit model using input data."""
        self.sanitize(codes)
        return self

    def sanitize(self, codes):
        """Sanitize model."""
        correct_indicies, structs = [], []
        for index, code in enumerate(codes):
            if self.check(code):
                correct_indicies.append(index)
                structs.append(self._encode(self.method(code)))
        return np.array(correct_indicies), structs

    def fit_sanitize(self, codes, **fit_params):
        """For the sake of speed-up."""
        return self.sanitize(codes)
