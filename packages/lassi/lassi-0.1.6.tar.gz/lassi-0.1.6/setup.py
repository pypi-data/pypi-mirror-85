# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'மூலம்'}

packages = \
['lassi_console',
 'லஸ்ஸி',
 'லஸ்ஸி._வெளியே',
 'லஸ்ஸி._வெளியே.lark',
 'லஸ்ஸி._வெளியே.lark.__pyinstaller',
 'லஸ்ஸி._வெளியே.lark.grammars',
 'லஸ்ஸி._வெளியே.lark.parsers',
 'லஸ்ஸி._வெளியே.lark.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'ennikkai>=1.2.1,<2.0.0',
 'lassi-ilakkanankal>=1.0.12,<2.0.0',
 'regex>=2020,<2021',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['lassi = lassi_console.console:run']}

setup_kwargs = {
    'name': 'lassi',
    'version': '0.1.6',
    'description': 'லஸ்ஸி',
    'long_description': None,
    'author': 'Julien Malard',
    'author_email': 'julien.malard@mail.mcgill.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://xn--5lcma2a9d.xn--xkc2dl3a5ee0h/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
