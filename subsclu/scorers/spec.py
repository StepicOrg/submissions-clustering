import logging

from subsclu import languages
from subsclu.exceptions import InvalidSpecError
from .error import ErrorScorer
from .ratio import RatioMetric

logger = logging.getLogger(__name__)

VALID_APPROACHES = "diff", "token"


def from_spec(language, approach):
    logger.info("creating scorer from spec with language={}, approach={}"
                .format(language, approach))
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
        raise InvalidSpecError("approach must be of the {}".format(VALID_APPROACHES))
