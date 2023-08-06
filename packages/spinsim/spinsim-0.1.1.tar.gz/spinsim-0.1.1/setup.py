# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spinsim', 'spinsim.utilities']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spinsim',
    'version': '0.1.1',
    'description': 'A package for simulating spin half and spin one quantum systems quickly and accurately using cuda parallelisation.',
    'long_description': None,
    'author': 'Alexander Tritt',
    'author_email': 'alexander.tritt@monash.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
