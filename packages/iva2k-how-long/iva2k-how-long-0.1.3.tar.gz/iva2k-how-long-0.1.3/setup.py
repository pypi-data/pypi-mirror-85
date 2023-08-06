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
    'version': '0.1.3',
    'description': 'A simple decorator to measure a function excecution time.',
    'long_description': 'iva2k_how_long\n==============\n\nSimple Decorator to measure a function execution time.\n\nVery lightweight project to get familiar with poetry publishing to PyPi, built from tutorial https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1\n\n\nExample\n_______\n\n.. code-block:: python\n\n    from iva2_how_long import timer\n\n\n    @timer\n    def some_function():\n        return [x for x in range(10_000_000)]\n        ',
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
