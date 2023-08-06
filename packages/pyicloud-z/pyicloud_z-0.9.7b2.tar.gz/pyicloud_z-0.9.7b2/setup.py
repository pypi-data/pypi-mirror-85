# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyicloud', 'pyicloud.services']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2019.11.28',
 'click>=6.0,<=7.1.1',
 'future>=0.18.2',
 'keyring>=8.0,<=9.3.1',
 'keyrings.alt>=1.0,<=3.2.0',
 'pytz>=2019.3',
 'requests>=2.20.0',
 'six>=1.14.0',
 'tzlocal==2.0.0']

setup_kwargs = {
    'name': 'pyicloud-z',
    'version': '0.9.7b2',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
