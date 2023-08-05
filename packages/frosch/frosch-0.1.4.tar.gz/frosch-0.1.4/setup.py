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
    'version': '0.1.4',
    'description': 'Better runtime error messages',
    'long_description': None,
    'author': 'Patrick Haller',
    'author_email': 'patrickhaller40@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
