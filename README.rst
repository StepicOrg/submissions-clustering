======================
submissions-clustering
======================

Fine tool to split code submissions into clusters.

------------
Installation
------------

Addititional deps
=================

- make
- pip

Pip
===

``pip install git+https://github.com/StepicOrg/submissions-clustering.git``

Working with
========

``make help`` for help. Then either ``build``, ``run`` or ``test``.

-----
Usage
-----

SetUp
=====

At first, we need to set things up. Customize your logger behavior:

>>> import logging
>>> logging.basicConfig(
...     level=logging.INFO,
...     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
... )

Training
========

Simple example of usage. Firslty, with filter out invalid py code. Then, ``.fit`` takes iterable of *(code, status)*,
fitting model and finding similarities. ``.neighbors`` gives ids of most similar correct code samples:

>>> import subsclu
>>> from subsclu.utils import read as read_utils
>>> submissions = read_utils.from_sl3("data/subs.sl3", nrows=3000)
>>> submissions = list(read_utils.filter_out_invalid(submissions, "python"))
>>> model = subsclu.from_spec("python", "ast")
>>> model.fit(submissions)
>>> print(len(model.neighbors([subs[0][0]])[0]))
300

Saving & Restoring
==================

Model class provide save and static load methods for faster and efficient model saving and loading:

>>> model.save("data/model.dump")
>>> del model
>>> model = subsclu.SubmissionsClustering.load("data/model.dump")

Default serializing machinery provided by joblib package from sklearn (for faster work with numpy matricies). Since
model is pickable object, you can use methods from pickle package (and also use with `django-picklefield`_):

.. _`django-picklefield`: https://pypi.python.org/pypi/django-picklefield

>>> from subsclu.utils import dump as dump_utils
>>> dump_utils.pickle_save(model, "data/model.dump")
>>> del model
>>> model = dump_utils.pickle_load("data/model.dump")

Evaluating
==========

Of course, we need to somehow evaluate performance of our model. For this we use scorers:

>>> from subsclu import scorers
>>> scorer = scorers.from_spec("python", "diff")

The overall score is compute as mean of diff between best metric and local best metric (within neighbors). Metric
evaluate how close is one code to another. We can speed-up the calculating using predefined array of best scores:

>>> scorer.score(model, submissions, presaved_score_path="data/best_metrics.dump")
0.013940358468805102

----
Test
----

You can either run:

``make test``

to run tests in current enviroment. Another option is:

``tox``

to test full build-test cycle in separate py34 venv.

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