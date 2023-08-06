# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextlib3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextlib3',
    'version': '3.10.0',
    'description': 'Backport of Python 3.10 standard library’s contextlib module to other python 3 versions',
    'long_description': '# contextlib3\n\n[![PyPI](https://img.shields.io/pypi/v/contextlib3)](https://pypi.org/project/contextlib3/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/contextlib3)](https://pypi.org/project/contextlib3/)\n[![PyPI License](https://img.shields.io/pypi/l/contextlib3)](https://pypi.org/project/contextlib3/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nBackport of Python 3.10 standard library’s contextlib module to other python 3 versions.\n',
    'author': 'Tom Gringauz',
    'author_email': 'tomgrin10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomgrin10/contextlib3',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
