from subsclu.scorers import Scorer


def test_scorer():
    scorer = Scorer.outof("python", "diff")
    assert isinstance(
        scorer,
        Scorer
    ), "basic instance check"

    assert hasattr(scorer, "score"), "has score method to score"
