# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pypi_client']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'diskcache>=5.0.3,<6.0.0',
 'lxml>=4.6.1,<5.0.0',
 'pypistats>=0.12.1,<0.13.0',
 'requests>=2.24.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.51.0,<5.0.0']

entry_points = \
{'console_scripts': ['pypi-client = pypi_client.cli:cli']}

setup_kwargs = {
    'name': 'pypi-client',
    'version': '0.1.2',
    'description': 'PyPI command-line tool',
    'long_description': 'PyPI client\n===========\n\n```\nUsage: pypi-client [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  auth-github  Log into GitHub\n  search       Search python package by name\n```',
    'author': 'Andrzej Bogdanowicz',
    'author_email': 'bahdanovich@rtbhouse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abahdanovich/pypi-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
