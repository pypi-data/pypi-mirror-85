# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bowline']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'bowline',
    'version': '0.1.2',
    'description': 'Configurable tools to easily pre and post process your data for data-science and machine learning.',
    'long_description': '-------\nBowline\n-------\n\nConfigurable tools to easily pre and post process your data for data-science and machine learning.\n\n=============\nWhy the name?\n=============\nAs data is quite hard to "wrangle" I thought what\'d be better to use then the name of a knot. So here we are, Bowline is a tool made for all your data wrangling needs.\n',
    'author': 'Marco Gancitano',
    'author_email': 'marco.gancitano97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mgancita/bowline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
