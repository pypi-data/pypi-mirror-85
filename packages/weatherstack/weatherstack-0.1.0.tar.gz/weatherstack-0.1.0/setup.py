# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weatherstack']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'weatherstack',
    'version': '0.1.0',
    'description': 'A Python wrapper around WeatherStack APIs',
    'long_description': None,
    'author': 'Morgan Kilgore',
    'author_email': 'mkilgore301@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
