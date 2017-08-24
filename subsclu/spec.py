# flake8: noqa
# pylint: skip-file
"""Module consist of model specifications."""

import logging

from subsclu.exceptions import InvalidSpec
from subsclu.languages import Language
from subsclu.model import SubmissionsClustering
from subsclu.pipe import *

__all__ = ["VALID_APPROACHES", "model_from_spec"]

logger = logging.getLogger(__name__)

VALID_APPROACHES = "diff", "token", "ast", "test"
"""Tuple of valid approaches."""


def model_from_spec(language, approach):
    """Create model from language and approach.

    Args:
        language (str): Name of language to use.
        approach (str): Approach to use.

    Returns:
        An instance of :class:`subsclu.model.SubmissionsCLustering`.

    """
    logger.info("creating model from spec with language %s, approach %s",
                language, approach)
    language = Language.outof(language)
    if approach == "diff":
        return SubmissionsClustering(
            preprocessor=CodePreprocessor(
                method=language.tokenize,
                check=language.check
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=SimpleClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "token":
        return SubmissionsClustering(
            preprocessor=CodePreprocessor(
                method=language.tokenize,
                check=language.check
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 3)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=SimpleClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "ast":
        return SubmissionsClustering(
            preprocessor=CodePreprocessor(
                method=language.astize,
                check=language.check
            ),
            vectorizer=make_pipeline(
                BagOfTrees(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=SimpleClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "test":
        return SubmissionsClustering(
            preprocessor=CodePreprocessor(
                method=language.astize,
                check=language.check
            ),
            vectorizer=make_pipeline(
                Token2Vec(),
                SumList(),
                Normalizer()
            ),
            clusterizer=SimpleClusterizer(),
            seeker=NNSeeker()
        )
    else:
        raise InvalidSpec("approach must be of the {}"
                          .format(VALID_APPROACHES))
