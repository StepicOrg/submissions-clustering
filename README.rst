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

Building
========

``make``

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

Example
=======

Simple example of using. ``.fit`` takes iterable of *(code, status)*, fitting model and finding
similarities. ``.neighbors`` gives ids of most similar code samples.

>>> import subsclu
>>> from subsclu.utils import read as read_utils
>>> model = subsclu.from_spec("python", "diff")
>>> subs = list(read_utils.from_sl3("data/subs.sl3", nrows=1000))
>>> model.fit(subs)
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

Articles
========

The entire project idea is based on `this article`_ "Deep Knowledge Tracing On Programming Exercises"

.. _`this article`: http://dl.acm.org/citation.cfm?id=3053985

``TODO``