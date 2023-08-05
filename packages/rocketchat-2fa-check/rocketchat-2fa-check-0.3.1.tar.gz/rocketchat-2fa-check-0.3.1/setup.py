# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rocketchat_2fa_check']

package_data = \
{'': ['*']}

install_requires = \
['click-pathlib>=2020.3.13,<2021.0.0',
 'click>=7.0,<8.0',
 'pymongo>=3.8,<4.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['rc-check-2fa = rocketchat_2fa_check.__main__:_run_main']}

setup_kwargs = {
    'name': 'rocketchat-2fa-check',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'Ulrich Petri',
    'author_email': 'github@ulo.pe',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
