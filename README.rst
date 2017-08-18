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
- java 1.8 to run `ASTScorer` server

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
>>> from subsclu import utils

>>> snn = sc.from_spec("python", "diff")
>>> subs = list(utils.from_sl3("data/subs.sl3", nrows=1000))
>>> snn.fit(subs)
>>> print(len(snn.neighbors([subs[0][0]])[0]))
300

Saving & Restoring
==================

Efficient save and load using joblib for faster work with numpy arrays.

>>> snn.save("data/snn.dump")
>>> del snn
>>> snn = sc.SubmissionsClustering.load("data/snn.dump")

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