.PHONY: help clean dev docs package test

init:
	pip install -e .
	pip install -r requirements_dev.txt

test:
	coverage run -m unittest discover -s tests -v

lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --ignore F401,F841,W504 --show-source
	# exit-zero treats all errors as warnings.
	flake8 . --count --exit-zero --max-complexity=10
