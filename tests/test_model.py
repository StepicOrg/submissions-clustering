import subsclu as sc


def test_outof():
    assert isinstance(
        sc.SubmissionsClustering.outof("python", "diff"),
        sc.SubmissionsClustering
    ), "check basic outof creation"
