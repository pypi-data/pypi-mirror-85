# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhstr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyhstr',
    'version': '0.2.0',
    'description': 'History suggest box for the standard Python shell, IPython, and bpython',
    'long_description': None,
    'author': 'adder46',
    'author_email': 'dedmauz69@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
