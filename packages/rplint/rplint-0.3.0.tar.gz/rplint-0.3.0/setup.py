# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rplint']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'rplint',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Jim Anderson',
    'author_email': 'jima.coding@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
