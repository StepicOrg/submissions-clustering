from subsclu import languages
from subsclu.utils import gdisk
from .ast import ASTScorer
from .ratio import RatioScorer

__all__ = ["ASTScorer", "RatioScorer"]

VALID_ARGS = ("python", "diff"), ("python", "token"), ("python", "ast")


def from_spec(language, approach):
    if (language, approach) == ("python", "diff"):
        return RatioScorer(method=lambda x: x)
    elif (language, approach) == ("python", "token"):
        return RatioScorer(method=languages.from_spec("python").asttokenize)
    elif (language, approach) == ("python", "ast"):
        return ASTScorer(patch_server_jar_path=gdisk.download_file("amorph-server.jar"))
    else:
        raise ValueError("language and approach must be of the {VALID_ARGS}")
