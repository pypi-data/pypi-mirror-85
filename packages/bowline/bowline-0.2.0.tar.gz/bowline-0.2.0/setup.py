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
    'version': '0.2.0',
    'description': 'Configurable tools to easily pre and post process your data for data-science and machine learning.',
    'long_description': '# Bowline\n\n![build](https://github.com/mgancita/bowline/workflows/Continuous%20Integration/badge.svg)\n[![PyPI version](https://badge.fury.io/py/bowline.svg)](https://badge.fury.io/py/bowline)\n![versions](https://img.shields.io/pypi/pyversions/bowline.svg)\n[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)\n![PyPI downloads](https://img.shields.io/github/downloads/mgancita/bowline/total)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nConfigurable tools to easily pre and post process your data for data-science and machine learning.\n\n## Quickstart\nThis will show you how to install and create a minimal implementation of `Bowline`. For more in-depth examples visit the [Official Docs](https://mgancita.github.io/bowline).\n\n### Installation\n```\n$ pip install bowline\n```\n\n### Minimal implementation\n```python\nfrom bowline import StandardPreprocessor\nimport pandas as pd\n\nraw_data = pd.read_csv(\'path/to/your/file\')\npreprocessor = StandardPrepreocessor(\n    data = data,\n    numerical_features = ["age", "capital-gain"],\n    binary_features = ["sex"],\n    categoric_features = ["occupation", "education"]\n)\nprocessed_data = preprocessor.process(target="sex")\n```\n',
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
