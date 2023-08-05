# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stockholm_data_manager',
 'stockholm_data_manager.core',
 'stockholm_data_manager.plugins',
 'stockholm_data_manager.sterile',
 'stockholm_data_manager.utils']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=14.0,<15.0', 'gspread>=3.6.0,<4.0.0', 'tqdm>=4.50.2,<5.0.0']

setup_kwargs = {
    'name': 'stockholm-data-manager',
    'version': '0.11.0',
    'description': 'Stockholm dataset manager.',
    'long_description': None,
    'author': 'Amresh Venugopal',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
