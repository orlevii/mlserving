.PHONY: help clean dev docs package test

init:
	pip install --upgrade pip
	pip install -e .[falcon]
	pip install -r requirements_dev.txt

test:
	coverage run --source ./mest -m unittest discover -s tests -v

lint:
	pip install flake8
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --builtins="__version__" --ignore F821
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --builtins="__version__" --ignore F821
