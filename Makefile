PSPPREFIX=python setup.py

all: reqs build

help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

reqs:	## Install all reqs from requirements.txt
	pip install -r requirements.txt

freeze:	## Freeze currect pip packages and place them into requirements.txt file
	pip freeze >requirements.txt

build:	## Build the project
	${PSPPREFIX} build
	${PSPPREFIX} sdist

run:	## Run main.py script
	python main.py

tests:	## Run tests
	${PSPPREFIX} test

tox:	## Run tox tests in separate venv
	tox

docs:	## Making Sphinx docs
	sphinx-apidoc -f -o docs/source subsclu/
	cd docs && make latexpdf

flake:	## Check if main package fit into flake standards
	${PSPPREFIX} flake8

clean:	## Clean-up the building output dirs
	${PSPPREFIX} clean
	rm -rf build dist *.egg-info .eggs .cache .tox
	make -C docs/ clean

.PHONY: all help reqs freeze build run tests tox docs flake clean