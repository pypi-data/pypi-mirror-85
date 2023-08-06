# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stream_tools']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'stream-tools',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Mattia Terenzi',
    'author_email': 'm.terenzi92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
