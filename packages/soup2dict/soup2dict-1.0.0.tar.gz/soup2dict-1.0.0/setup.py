# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soup2dict']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'classes>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'soup2dict',
    'version': '1.0.0',
    'description': 'Turns your beautifulsoup4 soup into python dictionary',
    'long_description': None,
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
