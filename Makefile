.PHONY: clean

venv:
	tox -e venv

test:
	tox -e test

clean:
	find -name '*.pyc' -delete
	find -name '__pycache__' -delete
	rm -rf .tox
	rm -rf venv
