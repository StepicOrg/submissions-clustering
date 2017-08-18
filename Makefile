PSPPREFIX=python setup.py

all: reqs build

reqs:
	pip install -r requirements.txt

freeze:
	pip freeze >requirements.txt

build:
	${PSPPREFIX} build
	${PSPPREFIX} sdist

flake:
	${PSPPREFIX} flake8

clean:
	${PSPPREFIX} clean
	rm -rf build dist *.egg-info

.PHONY: all reqs freeze build flake clean