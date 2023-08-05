# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymathalgos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymathalgos',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Adi58816',
    'author_email': 'adisalimgereev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
