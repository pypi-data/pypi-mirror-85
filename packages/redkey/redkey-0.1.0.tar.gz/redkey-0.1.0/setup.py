# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redkey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'redkey',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
