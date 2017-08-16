# submissions-clustering

## Installation

### Pip

`pip install git+https://github.com/StepicOrg/submissions-clustering.git`

### Building

`make`

### Addititional deps

java 1.8 to run `ASTScorer` server

## Usage

### Example

```python
>>> from sc import sc_from_spec
>>> from sc.utils import read_subs

>>> sc = sc_from_spec("python", "test")
>>> codes, statuses = read_subs.from_csv("data/step-12768-submissions.csv", nrows=1000)
>>> # codes, statuses = read_subs.from_sl3("data/subs.sl3"), number=3)
>>> print(len(sc.fit_neighbors(codes, statuses)[0]))
300
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
>>> from sc.scorers import scorer_from_spec

>>> plotter = plotter_from_spec("plotly")
>>> sc.plot_with(plotter, title="Test plot", path="plots/temp_plot.html")
```

## Test


**TODO**


## Useful Links

### Articles

* The entire project idea is based on [this article](http://dl.acm.org/citation.cfm?id=3053985 "Deep Knowledge Tracing On Programming Exercises")

**TODO**