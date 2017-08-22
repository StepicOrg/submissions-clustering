import subsclu


def test_instance():
    assert isinstance(subsclu.from_spec("python", "diff"), subsclu.SubmissionsClustering)
