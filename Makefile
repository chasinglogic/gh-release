# system python interpreter. used only to create virtual environment
PY = python3
BIN=poetry run

# make it work on windows too
ifeq ($(OS), Windows_NT)
    PY=python
endif


all: format lint test

poetry.lock: pyproject.toml
	poetry install

.PHONY: test
test: poetry.lock
	$(BIN) pytest

.PHONY: lint
lint: poetry.lock format
	$(BIN) flake8 github_release tests

.PHONY: format
format: poetry.lock
	$(BIN) black github_release tests
	$(BIN) isort github_release tests

.PHONY: release
release: poetry.lock
	poetry build
	poetry publish

.PHONY: clean
clean:
	rm -rf dist build
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
