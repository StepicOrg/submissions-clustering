from subsclu import languages
from .error import make_error
from .ratio import RatioMetric

VALID_ARGS = ("python", "diff"), ("python", "token")


def from_spec(language, approach):
    if (language, approach) == ("python", "diff"):
        return make_error(
            metric=RatioMetric(method=lambda x: x)
        )
    elif (language, approach) == ("python", "token"):
        return make_error(
            metric=RatioMetric(method=languages.from_spec("python").asttokenize)
        )
    else:
        raise ValueError("language and approach must be of the {}".format(VALID_ARGS))
