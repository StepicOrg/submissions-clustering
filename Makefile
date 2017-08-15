all: init build

init:
	pip install -r requirements.txt

build:
	python setup.py build

clean:
	python setup.py clean

.PHONY: all init build clean