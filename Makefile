SHELL:=/usr/bin/env bash

TESTS := tests/

ALL_TESTS := $(TESTS)

PYTHON_PATH ?= $(PWD)

# Allows direct coverage runs
ifeq ($(LIMIT),)
LIMIT := 50
endif

clean: # General repo cleanup
	@find . -name .pytest_cache | xargs rm -fr
	@find . -name __pycache__ | xargs rm -fr
	@find . -name .coverage | xargs rm -f
	@find . -name coverage.xml | xargs rm -f

wicked-clean: clean ## Remove all packages
	@pip freeze | xargs pip uninstall -y > /dev/null 2>&1 || true

deps: clean ## Install all dependencies
	@pip install -r requirements.dev && pip install -r requirements.txt

check: ## Run all checks
	@flake8 --exit-zero --ignore=E731,W503 --exclude $(TESTS) .

pylint: ## Run the pylinter
	@pylint --exit-zero --rcfile .pylintrc lib/ tests/

test: ## Run the tests
	@python -m pytest $(TESTS)

coverage: ## Check test coverage
	@python -m pytest --cov . --cov-config .coveragerc --cov-report term-missing --cov-report xml --cov-fail-under $(LIMIT) $(TESTS)

htmlcov: ## Create and open an HTML report of test coverage
	@python -m pytest --cov . --cov-config .coveragerc --cov-report html $(TESTS)
	rm -rf /tmp/htmlcov && mv htmlcov /tmp/
	open /tmp/htmlcov/index.html

stats: ## Generate code stats with radon
	@printf "Cyclomatic Complexity Report \n"
	@radon cc --total-average lib/ tests/
	@printf "#%.0s" {1..100}
	@printf "\n Maintainability Index Report \n"
	@radon mi -s --sort lib/ tests/

prcheck: wicked-clean deps check pylint test coverage stats ## Runs all checks before PR submission

.PHONY: help htmlcov

help:
  @awk 'BEGIN {FS = ":.*?## "} /^[a-zA_-]+:.*?## {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help