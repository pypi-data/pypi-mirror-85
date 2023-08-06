# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seekout',
 'seekout.alerts',
 'seekout.drivers',
 'seekout.objects',
 'seekout.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.24.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'seekout',
    'version': '0.1.2',
    'description': 'Library for parsing web pages',
    'long_description': None,
    'author': 'mauza',
    'author_email': 'mauza@mauza.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
