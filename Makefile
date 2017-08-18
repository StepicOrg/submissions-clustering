PSPPREFIX=python setup.py

all: reqs build

reqs:	## Install all reqs from requirements.txt
	pip install -r requirements.txt

freeze:	## Freeze currect pip packages and place them into requirements.txt file
	pip freeze >requirements.txt

build:	## Build the project
	${PSPPREFIX} build
	${PSPPREFIX} sdist

flake:	## Check if main package fit into flake standards
	${PSPPREFIX} flake8

clean:	## Clean-up the building output dirs
	${PSPPREFIX} clean
	rm -rf build dist *.egg-info

help:	## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: all reqs freeze build flake clean help