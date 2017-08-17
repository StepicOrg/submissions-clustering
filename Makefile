all: reqs build

reqs:
	pip install -r requirements.txt

build:
	python setup.py build

check:
	python setup.py check

freeze:
	pip freeze >requirements.txt

dir=sc/

flake:
	flake8 --max-line-length=99 ${dir}

clean:
	python setup.py clean

.PHONY: all reqs build freeze flake clean