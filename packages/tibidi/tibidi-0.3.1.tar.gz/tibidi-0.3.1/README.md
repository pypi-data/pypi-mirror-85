# tibidi

Dump your traceback into a file.

* Documentation: <https://gergelyk.github.io/python-tibidi>
* Repository: <https://github.com/gergelyk/python-tibidi>
* Package: <https://pypi.python.org/pypi/tibidi>
* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)
* License: [MIT](LICENSE)

## Requirements

This package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).

```sh
pyenv install 3.8.2
pyenv local 3.8.2
```

## Installation

```sh
pip install tibidi
```

## Usage

```sh
poetry run python tibidi/hello.py
```

## Development

```sh
# Preparing environment
pip install --user poetry  # unless already installed
poetry install

# Auto-formatting
poetry run docformatter -ri tibidi tests
poetry run isort -rc tibidi tests
poetry run yapf -r -i tibidi tests

# Checking coding style
poetry run flake8 tibidi tests

# Checking composition and quality
poetry run vulture tibidi tests
poetry run mypy tibidi tests
poetry run pylint tibidi tests
poetry run bandit tibidi tests
poetry run radon cc tibidi tests
poetry run radon mi tibidi tests

# Testing with coverage
poetry run pytest --cov tibidi --cov tests

# Rendering documentation
poetry run mkdocs serve

# Building package
poetry build

# Releasing
poetry version minor  # increment selected component
git commit -am "bump version"
git push
git tag ${$(poetry version)[2]}
git push --tags
poetry build
poetry publish
poetry run mkdocs build
poetry run mkdocs gh-deploy -b gh-pages
```

## Donations

If you find this software useful and you would like to repay author's efforts you are welcome to use following button:

[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)

