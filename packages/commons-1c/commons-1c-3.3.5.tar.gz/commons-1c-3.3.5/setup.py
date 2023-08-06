# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commons_1c']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0', 'cjk-commons>=3.5,<4.0', 'loguru>=0.5,<0.6']

setup_kwargs = {
    'name': 'commons-1c',
    'version': '3.3.5',
    'description': 'Commons for 1C:Enterprise',
    'long_description': None,
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cujoko/commons-1c',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
