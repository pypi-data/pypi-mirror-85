# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bl60x_flash']

package_data = \
{'': ['*'], 'bl60x_flash': ['contrib/*']}

install_requires = \
['pyserial>=3.4,<4.0', 'tqdm>=4.51.0,<5.0.0']

entry_points = \
{'console_scripts': ['bl60x-flash = bl60x_flash.main:main']}

setup_kwargs = {
    'name': 'bl60x-flash',
    'version': '0.1.3',
    'description': 'Flash tool for Bouffalo Labs BL60x UART bootloader',
    'long_description': None,
    'author': 'Stefan Schake',
    'author_email': 'stschake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
