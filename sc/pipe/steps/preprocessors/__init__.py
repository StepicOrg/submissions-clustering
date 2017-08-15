from .simple import *

__all__ = simple.__all__

VALID_LANGUAGES = "python",


def from_spec(language, method, **kwargs):
    if language == "python":
        return SimplePreprocessor(language=language, method=method, **kwargs)
    else:
        raise ValueError(f"language must be of the {VALID_LANGUAGES}")
