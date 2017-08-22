# flake8: noqa
from subsclu import languages
from subsclu.pipe import *
from .scnn import SubmissionsClustering

VALID_APPROACHES = "diff", "token", "ast", "test"


def from_spec(language, approach):
    language = languages.from_spec(language)
    if approach == "diff":
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                method=language.tokenize
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=StupidClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "token":
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                method=language.tokenize
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 3)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=StupidClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "ast":
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                method=language.astize
            ),
            vectorizer=make_pipeline(
                BagOfTrees(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=StupidClusterizer(),
            seeker=NNSeeker()
        )
    elif approach == "test":
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                method=language.astize
            ),
            vectorizer=make_pipeline(
                Token2Vec(),
                SumList(),
                Normalizer()
            ),
            clusterizer=StupidClusterizer(),
            seeker=NNSeeker()
        )
    else:
        raise ValueError("approach must be of the {}".format(VALID_APPROACHES))
