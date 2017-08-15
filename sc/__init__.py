from sc import languages
from sc.pipe.steps import *
from .sc import *

__all__ = sc.__all__

VALID_ARGS = ("python", "diff"),


def from_spec(language, approach):
    if language == "python" and approach == "diff":
        return SubmissionsClustering(
            preprocessor=SimplePreprocessor(
                language=languages.from_spec("python"),
                method="tokenize",
            ),
            vectorizer=make_pipeline(
                BagOfNgrams(ngram_range=(1, 2)),
                TfidfTransformer(),
                TruncatedSVD(n_components=100),
                Normalizer()
            ),
            clusterizer=AffinityPropagation(),
            seeker=NNSeeker()
        )
    else:
        raise ValueError(f"language and approach must be of the {VALID_ARGS}")
