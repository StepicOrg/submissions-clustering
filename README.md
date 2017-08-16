# submissions-clustering

## Installation

### Pip

`pip install git+https://github.com/StepicOrg/submissions-clustering.git`

### Building

`make`

## Usage

### Example

```python
>>> import sc
>>> from sc import utils

>>> snn = sc.from_spec("python", "diff")
>>> codes, statuses = utils.from_csv("data/step-12768-submissions.csv", nrows=1000)
>>> # codes, statuses = utils.from_sl3("data/subs.sl3", nrows=1000)
>>> snn.fit(codes, statuses)
>>> len(snn.neighbors(codes)[0])
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
>>> from sc import plotters

>>> plotter = plotters.from_spec("plotly2d")
>>> snn.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")
```

## Test


**TODO**


## Useful Links

### Articles

* The entire project idea is based on [this article](http://dl.acm.org/citation.cfm?id=3053985 "Deep Knowledge Tracing On Programming Exercises")

**TODO**