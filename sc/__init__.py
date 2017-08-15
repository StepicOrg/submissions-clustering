from sc.pipe.steps import *
from sc.pipe.steps import preprocessors
from .sc import *

__all__ = sc.__all__

VALID_ARGS = ("python", "diff"),


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
    else:
        raise ValueError(f"language and approach must be of the {VALID_ARGS}")
