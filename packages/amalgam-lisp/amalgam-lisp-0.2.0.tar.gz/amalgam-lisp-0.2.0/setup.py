# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amalgam']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'lark-parser>=0.10.1,<0.11.0',
 'prompt-toolkit>=3.0.7,<4.0.0']

entry_points = \
{'console_scripts': ['amalgam = amalgam.cli:amalgam_main']}

setup_kwargs = {
    'name': 'amalgam-lisp',
    'version': '0.2.0',
    'description': 'Lisp-like interpreted language implemented in Python',
    'long_description': '<p align="center">\n  <img src="./docs/logo.png"></img>\n</p>\n\n<p align="center">\n  LISP-like interpreted language implemented in Python.\n</p>\n\n<p align="center">\n  <img src="https://img.shields.io/travis/com/purefunctor/amalgam-lisp?label=build&logo=travis&style=flat-square" href="https://travis-ci.com/github/PureFunctor/amalgam-lisp">\n  <img src="https://img.shields.io/codecov/c/gh/purefunctor/amalgam-lisp?label=codecov&logo=codecov&style=flat-square" href="https://codecov.io/gh/PureFunctor/amalgam-lisp/">\n  <img src="https://img.shields.io/readthedocs/amalgam-lisp?style=flat-square" href="https://amalgam-lisp.readthedocs.io/">\n  <img src="https://img.shields.io/pypi/v/amalgam-lisp?style=flat-square" href="https://pypi.org/project/amalgam-lisp/">\n  <img src="https://img.shields.io/pypi/pyversions/amalgam-lisp?style=flat-square" href="https://pypi.org/project/amalgam-lisp/">\n</p>\n\n# Installation & Basic Usage\nThis package can be installed through PyPI:\n```bash\n$ pip install amalgam-lisp\n```\nThis makes the `amalgam` command-line script available.\n```bash\n$ amalgam                     # To invoke the REPL\n$ amalgam hello.am            # To load and run a file\n$ amalgam --expr="(+ 42 42)"  # To evaluate an expression\n```\n\n# Development Setup\nInstall the following dependencies:\n* Python 3.7 & 3.8\n* [Poetry](https://python-poetry.org)\n\nClone and then navigate to the repository:\n```bash\n$ git clone https://github.com/PureFunctor/amalgam-lisp.git\n$ cd amalgam-lisp\n```\n\nInstall the dependencies for the project:\n```bash\n$ poetry install\n$ poetry run pre-commit install\n```\n\n## Running Tests / Coverage Reports / Building Documentation\n`nox` is used for the automation of the execution of tests, which generates, combines, and reports coverage data for Python 3.7 and 3.8, as well as building documentation for the project.\n```bash\n$ poetry run nox\n```\n\nAlternatively, tests, coverage reports, and the documentation can be generated manually.\n```bash\n$ poetry run coverage run -m pytest\n$ poetry run coverage combine\n$ poetry run coverage report -m\n$ poetry run coverage html\n$ poetry run sphinx-build docs docs/build\n```\n',
    'author': 'PureFunctor',
    'author_email': 'purefunctor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PureFunctor/amalgam-lisp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
