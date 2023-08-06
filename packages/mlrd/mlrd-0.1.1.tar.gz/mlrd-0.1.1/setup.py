# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlrd']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['mlrd = mlrd.__main__:main']}

setup_kwargs = {
    'name': 'mlrd',
    'version': '0.1.1',
    'description': 'Mcgrill Lecture Recording Download (mlrd) tool',
    'long_description': None,
    'author': 'Brendan',
    'author_email': 'bshizzle1234@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brendan-kellam/mlrd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
