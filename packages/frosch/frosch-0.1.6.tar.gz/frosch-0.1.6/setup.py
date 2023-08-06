# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frosch']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.2,<3.0.0',
 'asttokens>=2.0.4,<3.0.0',
 'colorama>=0.4.4,<0.5.0',
 'stack-data>=0.1.0,<0.2.0',
 'yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['example = example.example:hello']}

setup_kwargs = {
    'name': 'frosch',
    'version': '0.1.6',
    'description': 'Better runtime error messages',
    'long_description': '# frosch - Runtime Error Debugger\n\n[![PyPI version](https://badge.fury.io/py/frosch.svg)](https://badge.fury.io/py/frosch)\n![Codecov](https://img.shields.io/codecov/c/github/HallerPatrick/frosch)\n\nBetter runtime error messages\n\nAre you also constantly seeing the runtime error message the\npython interpreter is giving you?\nIt lacks some color and more debug information!\n\n\nGet some good looking error tracebacks and beautifuly formatted\nlast line with all its last values *before* you crashed the program.\n\n<h1 align="center" style="padding-left: 20px; padding-right: 20px">\n  <img src="resources/showcase.png">\n</h1>\n\n\n## Installation\n\n```bash\n$ pip install frosch\n```\n\n## Usage\n\nCall the hook function at the beginning of your program.\n\n```python\n\nfrom frosch import hook\n\nhook()\n\nx = 3 + "String"\n\n```\n\n### Print Exceptions\n\nYou can also easily print your catched exceptions to stdout\n\n```python\n\nfrom frosch import print_exception\n\ntry:\n  x = [0, 1]\n  x[3]\nexcept IndexError as error:\n  print_exception(error)\n\n```\n\n\n# Configuration\n\n## Themes\n\nfrosch allows to use different themes for styling the output:\n\n| Themes   |          |          |               |             |      |\n|----------|----------|----------|---------------|-------------|------|\n| abap     | bw       | igor     | native        | rrt         | trac |\n| algol    | colorful | inkpot   | paraiso_dark  | sas         | vim  |\n| algol_nu | default  | lovelace | paraiso_light | solarized   | vs   |\n| arduino  | emacs    | manni    | pastie        | stata_dark  | xcode |\n| autumn   | friendly | monokai  | perldoc       | stata_light |      |\n| borland  | fruity   | murphy   | rainbow_dash  | tango       |      |\n\nUsage:\n\n```python\nfrom frosch import hook\n\nhook(theme="vim")\n````\n\n## OS Notifications\n\nBut wait there is more!\n\nRunning longer scripts in the background?\n\nJust add a title and/or message to the hook and it will you give a notification when your program \nis crashing.\n\n\n```python\n\nfrom frosch import hook\n\nhook(\n  theme="vs", # VSCode Theme\n  title="I crashed!",\n  message="Run Number #1444 is also crashing..."\n)\n```\n\nThis works on MacOS (`osascript`), Linux (`notify-send`) and Windows (`powershell`). \n\n\n\n# Contribution\n\n`frosch` uses [poetry](https://github.com/python-poetry/poetry) for build and dependency\nmanagement, so please install beforehand.\n\n## Setup\n\n```bash\n$ git clone https://github.com/HallerPatrick/frosch.git\n$ poetry install\n```\n\n## Run tests\n\n```python\n$ python -m pytest tests\n```\n',
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
