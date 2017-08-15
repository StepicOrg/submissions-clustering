from sc.pipe import *
from .sc import *

__all__ = sc.__all__

VALID_ARGS = ("python", "diff"), ("python", "test")


def from_spec(language, approach):
    if language == "python" and approach == "diff":
        return SubmissionsClustering(
            preprocessor=preprocessors.from_spec(
                language="python",
                method="asttokenize"
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=MiniBatchKMeans(n_clusters=20),
            seeker=NNSeeker()
        )
    elif language == "python" and approach == "test":
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
