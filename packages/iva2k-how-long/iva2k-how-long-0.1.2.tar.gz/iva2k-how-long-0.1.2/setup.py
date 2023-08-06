# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iva2k_how_long']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'iva2k-how-long',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'iva2k',
    'author_email': 'iva2k@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
