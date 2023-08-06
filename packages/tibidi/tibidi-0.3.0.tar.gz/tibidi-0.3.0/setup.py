# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbdebug', 'tbdump', 'tbpeep', 'tibidi']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.6.0,<2.0.0', 'peepshow>=0.2.3,<0.3.0']

setup_kwargs = {
    'name': 'tibidi',
    'version': '0.3.0',
    'description': 'Dump your traceback into a file.',
    'long_description': '# tibidi\n\nDump your traceback into a file.\n\n* Documentation: <https://gergelyk.github.io/python-tibidi>\n* Repository: <https://github.com/gergelyk/python-tibidi>\n* Package: <https://pypi.python.org/pypi/tibidi>\n* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)\n* License: [MIT](LICENSE)\n\n## Requirements\n\nThis package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).\n\n```sh\npyenv install 3.8.2\npyenv local 3.8.2\n```\n\n## Installation\n\n```sh\npip install tibidi\n```\n\n## Usage\n\n```sh\npoetry run python tibidi/hello.py\n```\n\n## Development\n\n```sh\n# Preparing environment\npip install --user poetry  # unless already installed\npoetry install\n\n# Auto-formatting\npoetry run docformatter -ri tibidi tests\npoetry run isort -rc tibidi tests\npoetry run yapf -r -i tibidi tests\n\n# Checking coding style\npoetry run flake8 tibidi tests\n\n# Checking composition and quality\npoetry run vulture tibidi tests\npoetry run mypy tibidi tests\npoetry run pylint tibidi tests\npoetry run bandit tibidi tests\npoetry run radon cc tibidi tests\npoetry run radon mi tibidi tests\n\n# Testing with coverage\npoetry run pytest --cov tibidi --cov tests\n\n# Rendering documentation\npoetry run mkdocs serve\n\n# Building package\npoetry build\n\n# Releasing\npoetry version minor  # increment selected component\ngit commit -am "bump version"\ngit push\ngit tag ${$(poetry version)[2]}\ngit push --tags\npoetry build\npoetry publish\npoetry run mkdocs build\npoetry run mkdocs gh-deploy -b gh-pages\n```\n\n## Donations\n\nIf you find this software useful and you would like to repay author\'s efforts you are welcome to use following button:\n\n[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)\n\n',
    'author': 'Grzegorz Krasoń',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gergelyk.github.io/python-tibidi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
