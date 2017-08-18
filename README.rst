======================
submissions-clustering
======================

Fine tool to split code submissions into clusters.

------------
Installation
------------

Pip
===

``pip install git+https://github.com/StepicOrg/submissions-clustering.git``

Addititional deps
=================

- make
- pip
- java 1.8 to run ``ASTScorer`` server

Building
========

``make``

-----
Usage
-----

Example
=======

Simple example of using. ``.fit`` takes iterable of *(code, status)*, fitting model and finding
similarities. ``.neighbors`` gives ids of most similar code samples.

>>> import subsclu
>>> from subsclu.utils import read as read_utils

>>> sc = subsclu.from_spec("python", "diff")
>>> subs = list(read_utils.from_sl3("data/subs.sl3", nrows=1000))
>>> sc.fit(subs)
>>> print(len(sc.neighbors([subs[0][0]])[0]))
300

Saving & Restoring
==================

Efficient save and load using joblib for faster work with numpy arrays.

>>> sc.save("data/snn.dump")
>>> del sc
>>> sc = subsclu.SubmissionsClustering.load("data/snn.dump")

----
Test
----

``TODO``

------------
Useful Links
------------

Articles
========

The entire project idea is based on `this article`_ "Deep Knowledge Tracing On Programming Exercises"

.. _`this article`: http://dl.acm.org/citation.cfm?id=3053985

``TODO``