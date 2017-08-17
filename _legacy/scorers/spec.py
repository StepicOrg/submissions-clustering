from sc.languages import from_spec
from sc.utils.gdisk import download_file
from .ast import *
from .ratio import *

__all__ = ["scorer_from_spec"]

VALID_ARGS = ("python", "diff"), ("python", "token"), ("python", "ast")


def scorer_from_spec(language, approach):
    if (language, approach) == ("python", "diff"):
        return RatioScorer(method=lambda x: x)
    elif (language, approach) == ("python", "token"):
        return RatioScorer(method=from_spec("python").asttokenize)
    elif (language, approach) == ("python", "ast"):
        return ASTScorer(patch_server_jar_path=download_file("amorph-server.jar"))
    else:
        raise ValueError("language and approach must be of the {VALID_ARGS}")
