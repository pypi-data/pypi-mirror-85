# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frog_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'frog-lib',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Frog Dev',
    'author_email': 'dev@frog-mining.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
