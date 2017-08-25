"""Module consist of scorers specifications."""

import logging

from subsclu.exceptions import InvalidSpec
from subsclu.languages import Language
from subsclu.scorers.error import ErrorScorer
from subsclu.scorers.ratio import RatioMetric

__all__ = ["VALID_APPROACHES", "scorer_from_spec"]

logger = logging.getLogger(__name__)

VALID_APPROACHES = "diff", "token"
"""Tuple of valie approaches."""


def scorer_from_spec(language, approach):
    """Create scorer from language and approach.

    Args:
        language (str): Name of language to use.
        approach (str): Approach to use.

    Returns:
        An instance of :class:`subsclu.scorers.base.Scorer`.

    """
    logger.info("creating scorer from spec with language %s, approach %s",
                language, approach)
    language = Language.outof(language)
    if approach == "diff":
        return ErrorScorer(
            metric=RatioMetric(
                method=lambda x: x
            ),
            check=language.check
        )
    elif approach == "token":
        return ErrorScorer(
            metric=RatioMetric(
                method=language.tokenize
            ),
            check=language.check
        )
    else:
        raise InvalidSpec("approach must be of the {}"
                          .format(VALID_APPROACHES))
