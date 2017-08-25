import numpy as np

from subsclu.pipe import *


def test_clusterizers():
    clusterizer = SimpleClusterizer()
    assert np.array_equal(
        clusterizer.fit_predict(np.arange(5)),
        -np.ones(5)
    ), "should give -1 label for each sample"


def test_vectorizers():
    sum_ = SumList()
    assert np.array_equal(
        sum_.fit_transform(
            np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        ),
        np.array([[4, 6], [12, 14]])
    ), "sum should working correct"

    mean = MeanList()
    assert np.array_equal(
        mean.fit_transform(
            np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        ),
        np.array([[2, 3], [6, 7]])
    ), "mean should working correct"


def test_commons():
    pipeline = make_pipeline(SumList(), MeanList())
    assert len(pipeline.steps) == 2, "two pipe ops"


def test_preprocessors():
    preprocessor = StupidPreprocessor()
    output = preprocessor.fit_sanitize(["code1", "code2"])
    assert len(output) == 2, "two codes as input, same at output"


def test_reducers():
    reducer = PCA(n_components=2)
    output = reducer.fit_transform(np.random.rand(5, 4))
    assert output.shape == (5, 2), "shape correctness"


def test_seekers():
    assert issubclass(NNSeeker, BaseEstimator), "sub check"
