from sc.pipe import *
from .sc import *

__all__ = ["sc_from_spec"]

VALID_ARGS = ("python", "diff"), ("python", "ast"), ("python", "test")


def sc_from_spec(language, approach):
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
    elif (language, approach) == ("python", "ast"):
        return sc_from_spec("python", "diff")
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
        raise ValueError(f"language and approach must be of the {VALID_ARGS}")
