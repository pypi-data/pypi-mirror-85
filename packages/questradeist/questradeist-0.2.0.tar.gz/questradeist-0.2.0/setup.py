# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['questradeist']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'questradeist',
    'version': '0.2.0',
    'description': 'A library for interacting with the Questrade API.',
    'long_description': None,
    'author': 'Chayim I. Kirshen',
    'author_email': 'c@kirshen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
