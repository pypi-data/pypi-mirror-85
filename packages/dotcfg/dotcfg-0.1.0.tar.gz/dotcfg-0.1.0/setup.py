# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotcfg']

package_data = \
{'': ['*']}

install_requires = \
['python-box>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'dotcfg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alex Cano',
    'author_email': 'alexjcano1994@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
