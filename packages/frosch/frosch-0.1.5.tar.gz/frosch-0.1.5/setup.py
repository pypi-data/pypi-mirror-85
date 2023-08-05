# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frosch']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.2,<3.0.0', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['example = example:example']}

setup_kwargs = {
    'name': 'frosch',
    'version': '0.1.5',
    'description': 'Better runtime error messages',
    'long_description': '# frosch - Runtime Error Debugger\n\n[![PyPI version](https://badge.fury.io/py/frosch.svg)](https://badge.fury.io/py/frosch)\n![Codecov](https://img.shields.io/codecov/c/github/HallerPatrick/frosch)\n\nBetter runtime error messages \n\nAre you also constantly seeing the runtime error message the \npython interpreter is giving you?\nIt lacks some color and more debug information!\n\n\nGet some good looking error tracebacks and beautifuly formatted\nlast line with all its last values *before* you crashed the program.\n\n<h1 align="center">\n  <img src="showcase.png">\n</h1>\n\n\n## Installation\n\n```bash\n$ pip install frosch\n\n```\n\n## Usage \n\n\nCall the hook function at the beginning of your program.\n\n```python\n\nfrom frosch import hook\n\nhook()\n\nx = 3 + "String"\n\n```\n\n## Contribution\n\n`frosch` uses [poetry](https://github.com/python-poetry/poetry) for build and dependency\nmanagement, so please install beforehand.\n\n### Setup\n\n```bash\n$ git clone https://github.com/HallerPatrick/frosch.git\n$ poetry install\n```\n\n### Run tests\n\n```python\n$ python -m pylint tests\n```\n',
    'author': 'Patrick Haller',
    'author_email': 'patrickhaller40@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HallerPatrick/frosch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
