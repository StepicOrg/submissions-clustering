# flake8: noqa
from subsclu.pipe import *
from .scnn import SubmissionsClustering

VALID_ARGS = ("python", "diff"), ("python", "token"), ("python", "ast"), ("python", "test")


def from_spec(language, approach):
    if (language, approach) == ("python", "diff"):
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                language="python",
                method="asttokenize"
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
    elif (language, approach) == ("python", "token"):
        return from_spec("python", "diff")
    elif (language, approach) == ("python", "ast"):
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                language="python",
                method="astize"
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
    elif (language, approach) == ("python", "test"):
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                language="python",
                method="tokenize"
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
        raise ValueError("language and approach must be of the {}".format(VALID_ARGS))
