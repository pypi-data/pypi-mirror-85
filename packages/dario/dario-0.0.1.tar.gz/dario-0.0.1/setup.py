# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dario']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

extras_require = \
{'uvloop': ['uvloop>=0.14.0,<0.15.0']}

entry_points = \
{'console_scripts': ['dario = dario.cli:main']}

setup_kwargs = {
    'name': 'dario',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Lukáš Kubiš',
    'author_email': 'contact@lukaskubis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukaskubis/dario',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
