# submissions-clustering

## Installation

`pip install git+https://github.com/StepicOrg/submissions-clustering.git`

## Usage

```python
>>> from sc.sc import SubmissionsClustering
>>> from sc.utils import from_csv

>>> sc = SubmissionsClustering.from_str("python", "diff")
>>> codes, statuses = from_csv("data/step-12768-submissions.csv", nrows=1000)
>>> print(len(sc.fit_neighbors(codes, statuses)[0]))
200
```

Stages:

```python
# 1: Preprocessor
# 2: Vectorizer
# 3: Clusterizer
# 4: Seeker
```

### Visualization

```python
>>> from sc.plotters import PlotlyPlotter

>>> plotter = PlotlyPlotter()
>>> sc.plot_with(plotter)
```

## Test


**TODO**


## Useful Links

### Articles

* The entire project idea is based on [this article](http://dl.acm.org/citation.cfm?id=3053985 "Deep Knowledge Tracing On Programming Exercises")

**TODO**