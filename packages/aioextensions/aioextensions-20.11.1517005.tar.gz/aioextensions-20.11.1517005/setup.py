# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioextensions']

package_data = \
{'': ['*']}

install_requires = \
['uvloop']

setup_kwargs = {
    'name': 'aioextensions',
    'version': '20.11.1517005',
    'description': 'High performance functions to work with the async IO',
    'long_description': '# Python Asyncio Extensions\n\n[![Release](\nhttps://img.shields.io/pypi/v/aioextensions?color=success&label=Release&style=flat-square)](\nhttps://pypi.org/project/aioextensions)\n[![Documentation](\nhttps://img.shields.io/badge/Documentation-click_here!-success?style=flat-square)](\nhttps://kamadorueda.github.io/aioextensions/)\n[![Downloads](\nhttps://img.shields.io/pypi/dm/aioextensions?label=Downloads&style=flat-square)](\nhttps://pypi.org/project/aioextensions)\n[![Status](\nhttps://img.shields.io/pypi/status/aioextensions?label=Status&style=flat-square)](\nhttps://pypi.org/project/aioextensions)\n[![Coverage](\nhttps://img.shields.io/badge/Coverage-100%25-success?style=flat-square)](\nhttps://kamadorueda.github.io/aioextensions/)\n[![License](\nhttps://img.shields.io/pypi/l/aioextensions?color=success&label=License&style=flat-square)](\nhttps://github.com/kamadorueda/aioextensions/blob/latest/LICENSE.md)\n',
    'author': 'Kevin Amado',
    'author_email': 'kamadorueda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kamadorueda.github.io/aioextensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
