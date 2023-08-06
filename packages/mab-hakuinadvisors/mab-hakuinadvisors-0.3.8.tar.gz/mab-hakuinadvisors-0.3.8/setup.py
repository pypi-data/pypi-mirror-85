# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mab']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mab-hakuinadvisors',
    'version': '0.3.8',
    'description': 'Multiarm bandit solutions',
    'long_description': None,
    'author': 'Alexey',
    'author_email': 'butirev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
