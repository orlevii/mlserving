.PHONY: help clean dev docs package test

help:
	@echo "This project assumes that an active Python virtualenv is present."
	@echo "The following make targets are available:"
	@echo "	 dev 	install all deps for dev env"
	@echo "  docs	create pydocs for all relveant modules"
	@echo "	 test	run all tests with coverage"

clean:
	rm -rf dist/*

dev:
	pip install --upgrade pip
	pip install coverage
	pip install -r requirements.txt
	pip install -e .

upload:
	python setup.py sdist upload -r local

test:
	coverage run -m unittest discover -v
	rm .coverage
