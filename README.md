# submissions-clustering

## Installation

### Pip

`pip install git+https://github.com/StepicOrg/submissions-clustering.git`

### Building

`make`

## Usage

### Example

```python
>>> from sc.sc import SubmissionsClustering
>>> from sc.utils import from_csv

>>> sc = SubmissionsClustering.from_str("python", "diff")
>>> codes, statuses = from_csv("data/step-12768-submissions.csv", nrows=1000)
>>> print(len(sc.fit_neighbors(codes, statuses)[0]))
200
```

### Steps

```python
# 1: Preprocessor
# 2: Vectorizer
# 3: Clusterizer
# 4: Seeker
```

### Visualization

```python
>>> sc = SubmissionsClustering.from_str("python", "diff")
>>> codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
>>> sc.fit(codes, statuses)

>>> plotter = plotters.from_spec("plotly")
>>> sc.plot_with(plotter, title="Test plotting", path="plots/temp_plot.html")
```

## Test


**TODO**


## Useful Links

### Articles

* The entire project idea is based on [this article](http://dl.acm.org/citation.cfm?id=3053985 "Deep Knowledge Tracing On Programming Exercises")

**TODO**