.PHONY: all develop test lint clean doc format

# The source directory
SRC=extranet

# The package name
PKG=extranet


all: test lint

#
# Setup
#
develop: install-deps activate-pre-commit configure-git

install-deps:
	@echo "--> Installing dependencies"
	pip install -U pip setuptools wheel
	poetry install

activate-pre-commit:
	@echo "--> Activating pre-commit hook"
	pre-commit install

configure-git:
	@echo "--> Configuring git"
	git config branch.autosetuprebase always


#
# testing & checking
#
test-all: test test-readme

test:
	@echo "--> Running Python tests"
	pytest --ff -x -p no:randomly
	@echo ""

test-randomly:
	@echo "--> Running Python tests in random order"
	pytest
	@echo ""

test-with-coverage:
	@echo "--> Running Python tests"
	py.test --cov $(PKG)
	@echo ""

test-with-typeguard:
	@echo "--> Running Python tests with typeguard"
	pytest --typeguard-packages=${PKG}
	@echo ""

vagrant-tests:
	vagrant up
	vagrant ssh -c /vagrant/deploy/vagrant_test.sh


#
# Various Checkers
#
lint: lint-py lint-js lint-rst lint-doc

lint-ci: lint

lint-all: lint lint-mypy lint-bandit

lint-py:
	@echo "--> Linting Python files /w flake8"
	flake8 $(SRC)
	@echo ""

lint-mypy:
	@echo "--> Typechecking Python files w/ mypy"
	mypy $(SRC)
	@echo ""

lint-travis:
	@echo "--> Linting .travis.yml files"
	travis lint --no-interactive
	@echo ""

lint-rst:
	@echo "--> Linting .rst files"
	rst-lint *.rst
	@echo ""

lint-doc:
	@echo "--> Linting doc"
	@echo "TODO"
	#sphinx-build -W -b dummy docs/ docs/_build/
	#sphinx-build -b dummy docs/ docs/_build/
	@echo ""

lint-js:
	echo "TODO"

#
# Formatting
#
format: format-py format-js

format-py:
	docformatter -i -r ${SRC}
	black .
	isort .

format-js:
	echo "TODO"


#
# Everything else
#
install:
	poetry install

doc: doc-html doc-pdf

doc-html:
	sphinx-build -W -b html docs/ docs/_build/html

doc-pdf:
	sphinx-build -W -b latex docs/ docs/_build/latex
	make -C docs/_build/latex all-pdf

clean:
	rm -f **/*.pyc
	find . -type d -empty -delete
	rm -rf *.egg-info *.egg .coverage .eggs .cache .mypy_cache .pyre \
		.pytest_cache .pytest .DS_Store  docs/_build docs/cache docs/tmp \
		dist build pip-wheel-metadata junit-*.xml htmlcov coverage.xml

tidy: clean
	rm -rf .tox .nox .dox .travis-solo
	rm -rf node_modules
	rm -rf instance

update-pot:
	# _n => ngettext, _l => lazy_gettext
	python setup.py extract_messages update_catalog compile_catalog

update-deps:
	pip install -U pip setuptools wheel
	poetry update
	poetry export --without-hashes -o requirements.txt

publish: clean
	git push --tags
	poetry build
	twine upload dist/*
