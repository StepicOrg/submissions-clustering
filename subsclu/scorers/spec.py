from subsclu import languages
from .error import ErrorScorer
from .ratio import RatioMetric

VALID_APPROACHES = "diff", "token"


def from_spec(language, approach):
    language = languages.from_spec(language)
    if approach == "diff":
        return ErrorScorer(
            metric=RatioMetric(
                method=lambda x: x
            )
        )
    elif approach == "token":
        return ErrorScorer(
            metric=RatioMetric(
                method=language.tokenize
            )
        )
    else:
        raise ValueError("approach must be of the {}".format(VALID_APPROACHES))
