import subsclu
from subsclu import spec as model_spec
from subsclu.languages import spec as languages_spec

LANGUAGES = languages_spec.VALID_NAMES
APPROACHES = model_spec.VALID_APPROACHES


def test_instance():
    for language, approach in zip(LANGUAGES, APPROACHES):
        assert isinstance(subsclu.from_spec(language, approach), subsclu.SubmissionsClustering)
