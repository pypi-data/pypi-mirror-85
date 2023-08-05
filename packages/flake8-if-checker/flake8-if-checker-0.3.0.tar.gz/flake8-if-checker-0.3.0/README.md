[![Build Status](https://travis-ci.org/danie1k/python-flake8-if-checker.svg?branch=master)](https://travis-ci.org/danie1k/python-flake8-if-checker)
[![Code Coverage](https://codecov.io/gh/danie1k/python-flake8-if-checker/branch/master/graph/badge.svg?token=y4x0mbm2XT)](https://codecov.io/gh/danie1k/python-flake8-if-checker)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-if-checker)](https://pypi.org/project/flake8-if-checker/)
[![PyPI](https://img.shields.io/pypi/v/flake8-if-checker)](https://pypi.org/project/flake8-if-checker/)
[![MIT License](https://img.shields.io/github/license/danie1k/python-flake8-if-checker)](https://github.com/danie1k/python-flake8-if-checker/blob/master/LICENSE)
[![Automatic PyPI Release](https://github.com/danie1k/python-flake8-if-checker/workflows/PyPi%20Release/badge.svg)](https://github.com/danie1k/python-flake8-if-checker/actions)

# flake8-if-checker

[Flake8](https://pypi.org/project/flake8/)'s `IF` statement complexity linter plugin.


## Table of Contents

1. [About the Project](#about-the-project)
1. [Installation](#installation)
1. [Configuration](#configuration)
1. [Known issues](#known-issues)
1. [License](#license)


## About the Project

This plugins adds one new flake8 warning.

`IF01` Too many conditions in IF/ELIF Statement/Expression.


## Installation

```
pip install flake8-if-checker
```

## Configuration

If using the select [option from flake8](http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-select)
be sure to enable the `IF` category as well.


## Known issues

- In Python 3.8 does not work with flake8 < 3.8
- Does not work with Python 3.9


## License

MIT
