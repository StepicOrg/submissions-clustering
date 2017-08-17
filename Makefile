all: init build

init:
	pip install -r requirements.txt

build:
	python setup.py build

freeze:
	pip freeze >requirements.txt

dir=sc/

flake:
	flake8 --max-line-length=99 ${dir}

clean:
	python setup.py clean

.PHONY: all init build freeze flake clean