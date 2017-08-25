PSPPREFIX=python setup.py

all: reqs build

help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

reqs:	## Install all reqs from requirements.txt
	pip install -r requirements.txt

build:	## Build the project
	${PSPPREFIX} build
	${PSPPREFIX} sdist

DIR=subsclu/

check:	## Runs flake8 and pylint checks (use can specify DIR to check)
	flake8 ${DIR}
	pylint ${DIR}

test:	## Run tests (see .tox for more info)
	tox

run:	## Run main.py script
	python main.py

doc:	## Making Sphinx docs
	sphinx-apidoc -f -o docs/source subsclu/
	cd docs && make latexpdf
	open docs/_build/latex/*.pdf

clean:	## Clean-up the building output dirs
	${PSPPREFIX} clean
	rm -rf build dist *.egg-info .eggs .cache
	make -C docs/ clean

.PHONY: all help reqs build check test run doc clean