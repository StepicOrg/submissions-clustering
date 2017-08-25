======================
submissions-clustering
======================

Fine tool to split code submissions into clusters.

------------
Installation
------------

Dependencies
============

1. **make**
2. **python** of version *3.4* or more.
3. **pip**

Pip
===

``pip install git+https://github.com/StepicOrg/submissions-clustering.git``

Locally
=======

1. ``git clone https://github.com/StepicOrg/submissions-clustering``
2. ``make reqs``
3. ``make build``

You can run ``make help`` for list of avialible deps. Some of them provided just for convinience. For example, you can
run ``make run`` to execute **main.py** script or run ``make check`` to run python static code checkers.

-----
Usage
-----

Setting Up
==========

At first, we need to set things up. Customize your logger behavior:

>>> import logging
>>> logging.basicConfig(
...     level=logging.INFO,
...     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
... )

Training
========

Simple example of usage. Firstly, we read our submissions as iterable *(code : str, status : str)* for some source. Then
we create a model from specification (langauge and approach). Then, we feed submission into model (the training goes
here). Lastly, we predict ids of first 5 neighbors for first code sample:

>>> import subsclu as sc
>>> from subsclu.utils import read as read_utils
>>> submissions = list(read_utils.from_sl3("data/subs.sl3", nrows=3000))
>>> model = sc.SubmissionsClustering.outof("python", "ast")
>>> model.fit(submissions)
>>> model.neighbors([submissions[0][0]])[0][:5]
array([   0, 2308, 1686,  460,  643])

Saving & Restoring
==================

Model class provide save and static load methods for faster and efficient model saving and loading:

>>> model.save("data/model.dump")
>>> del model
>>> model = sc.SubmissionsClustering.load("data/model.dump")

Default serializing machinery provided by joblib package from sklearn (for faster work with numpy matricies). Since
model is pickable object, you can use methods from pickle package (and also use with `django-picklefield`_):

.. _`django-picklefield`: https://pypi.python.org/pypi/django-picklefield

>>> from subsclu.utils import dump as dump_utils
>>> dump_utils.pickle_save(model, "data/model.dump")
>>> del model
>>> model = dump_utils.pickle_load("data/model.dump")

Evaluating
==========

Of course, we need to somehow evaluate performance of our model. For this purpose we gonna use scorers. Here we create
on of them from specification (language and testing approach). Scorer instance has *score(model, submissions, **kwargs)*
method to calculate of how good model (unfitted) perform on given submissions:

>>> from subsclu.scorers import Scorer
>>> scorer = Scorer.outof("python", "diff")
>>> hasattr(scorer, "score")
True

Scorer uses metric isntance inside, that measure of how close one code to another. The overall score is computed as mean
of diff between best metric and local best metric (within neighbors). Metric evaluate how close is one code to another.
We can speed-up the calculating using predefined array of best scores:

>>> scorer.score(model, submissions, presaved_score_path="data/best_metrics.dump")
0.013940358468805102

Spec and creating custom
========================

To see list of languages run:

>>> from subsclu.languages.spec import VALID_NAMES
>>> VALID_NAMES
('python',)

Same goes for approaches and other stuff:

>>> from subsclu.spec import VALID_APPROACHES
>>> VALID_APPROACHES
('diff', 'token', 'ast', 'test')

If you dont satisfied with predefined in spec set of things, you can define you own. See **subsclu** package subpackages
for more info on that.

----
Test
----

Run ``make test`` to start full build-test cycle in separate py34 venv using **tox**.

---
Doc
---

Run ``make doc`` to get pdf file of full package documentation.

------------
Useful Links
------------

Node embedding tensorboard
==========================

`Here <https://goo.gl/vUDr5U>`_ you can find embedding for AST nodes visualization in tensorboard.

Articles
========

The entire project idea is based on `this article <http://dl.acm.org/citation.cfm?id=3053985>`_.

I am also use `this <https://arxiv.org/pdf/1409.3358.pdf>`_,
`this <http://www.cs.cornell.edu/~kilian/papers/wmd_metric.pdf>`_, and
`that <https://pdfs.semanticscholar.org/5260/66e8c1007dd526eb4a7b89a925b95c6564f5.pdf>`_.