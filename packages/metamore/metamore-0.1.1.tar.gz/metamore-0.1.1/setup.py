# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metamore', 'metamore.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'piexif>=1.1.3,<2.0.0']

entry_points = \
{'console_scripts': ['mm = metamore.main:cli']}

setup_kwargs = {
    'name': 'metamore',
    'version': '0.1.1',
    'description': 'Metamore is a command line tool that helps you manage your metadata.',
    'long_description': None,
    'author': 'voukau',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
