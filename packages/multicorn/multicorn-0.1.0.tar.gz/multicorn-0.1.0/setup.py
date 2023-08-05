# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multicorn']

package_data = \
{'': ['*']}

install_requires = \
['backports.interpreters>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'multicorn',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'An Long',
    'author_email': 'aisk1988@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
