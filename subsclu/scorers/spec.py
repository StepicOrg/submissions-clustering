from subsclu import languages
from .error import ErrorScorer
from .ratio import RatioMetric


def from_spec(language, approach):
    method = languages.from_spec(language)[approach]
    return ErrorScorer(
        metric=RatioMetric(
            method=method
        )
    )
