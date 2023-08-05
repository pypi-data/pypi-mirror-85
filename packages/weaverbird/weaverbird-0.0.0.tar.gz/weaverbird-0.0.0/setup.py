# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weaverbird', 'weaverbird.steps']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.3,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'weaverbird',
    'version': '0.0.0',
    'description': 'Pandas engine for weaverbird data pipelines',
    'long_description': None,
    'author': 'Toucan Toco',
    'author_email': 'dev+weaverbird@toucantoco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
