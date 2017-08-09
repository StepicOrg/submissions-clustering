# submissions-clustering

## Installation

`pip install -r requirements.txt`


## Usage


```python
method = Method.from_predefined("python", "diff")
ss = SubmissionsSimilarity(method=method)
ss.fit(pd.read_csv("...")["code"])
ss.neighbors("...")
```

Stages:

```python
# 1: Preprocessor
# 2: Vectorizer
# 3: Clusterizer
```


## Test


**TODO**


## Useful Links

### Articles

* The entire project idea is based on [this article](http://dl.acm.org/citation.cfm?id=3053985 "Deep Knowledge Tracing On Programming Exercises")

**TODO**