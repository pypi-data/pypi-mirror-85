<p align="center">
  <img src="./docs/logo.png"></img>
</p>

<p align="center">
  LISP-like interpreted language implemented in Python.
</p>

<p align="center">
  <img src="https://img.shields.io/travis/com/purefunctor/amalgam-lisp?label=build&logo=travis&style=flat-square" href="https://travis-ci.com/github/PureFunctor/amalgam-lisp">
  <img src="https://img.shields.io/codecov/c/gh/purefunctor/amalgam-lisp?label=codecov&logo=codecov&style=flat-square" href="https://codecov.io/gh/PureFunctor/amalgam-lisp/">
  <img src="https://img.shields.io/readthedocs/amalgam-lisp?style=flat-square" href="https://amalgam-lisp.readthedocs.io/">
  <img src="https://img.shields.io/pypi/v/amalgam-lisp?style=flat-square" href="https://pypi.org/project/amalgam-lisp/">
  <img src="https://img.shields.io/pypi/pyversions/amalgam-lisp?style=flat-square" href="https://pypi.org/project/amalgam-lisp/">
</p>

# Installation & Basic Usage
This package can be installed through PyPI:
```bash
$ pip install amalgam-lisp
```
This makes the `amalgam` command-line script available.
```bash
$ amalgam                     # To invoke the REPL
$ amalgam hello.am            # To load and run a file
$ amalgam --expr="(+ 42 42)"  # To evaluate an expression
```

# Development Setup
Install the following dependencies:
* Python 3.7 & 3.8
* [Poetry](https://python-poetry.org)

Clone and then navigate to the repository:
```bash
$ git clone https://github.com/PureFunctor/amalgam-lisp.git
$ cd amalgam-lisp
```

Install the dependencies for the project:
```bash
$ poetry install
$ poetry run pre-commit install
```

## Running Tests / Coverage Reports / Building Documentation
`nox` is used for the automation of the execution of tests, which generates, combines, and reports coverage data for Python 3.7 and 3.8, as well as building documentation for the project.
```bash
$ poetry run nox
```

Alternatively, tests, coverage reports, and the documentation can be generated manually.
```bash
$ poetry run coverage run -m pytest
$ poetry run coverage combine
$ poetry run coverage report -m
$ poetry run coverage html
$ poetry run sphinx-build docs docs/build
```
