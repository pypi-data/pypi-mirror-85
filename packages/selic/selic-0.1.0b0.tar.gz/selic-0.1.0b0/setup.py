# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selic']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'selic',
    'version': '0.1.0b0',
    'description': 'Fetch SELIC data',
    'long_description': None,
    'author': 'tilacog',
    'author_email': 'tilacog@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tilacog/selic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
