from sc.languages import language_from_spec
from sc.utils.gdfiles import gdfile_from_spec
from .ast import *
from .ratio import *

__all__ = ["scorer_from_spec"]

VALID_ARGS = ("python", "diff"), ("python", "token"), ("python", "ast")


def scorer_from_spec(language, approach):
    if (language, approach) == ("python", "diff"):
        return RatioScorer(method=lambda x: x)
    elif (language, approach) == ("python", "token"):
        return RatioScorer(method=language_from_spec("python").asttokenize)
    elif (language, approach) == ("python", "ast"):
        return ASTScorer(patch_server_jar_path=gdfile_from_spec("amorph-server.jar"))
    else:
        raise ValueError(f"language and approach must be of the {VALID_ARGS}")
