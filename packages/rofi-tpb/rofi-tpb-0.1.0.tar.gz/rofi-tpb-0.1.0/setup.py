# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rofi_tpb']

package_data = \
{'': ['*']}

install_requires = \
['dynmen>=0.1.5,<0.2.0',
 'lxml>=4.6.1,<5.0.0',
 'tpblite>=0.6,<0.7',
 'traitlets>=5.0.4,<6.0.0']

entry_points = \
{'console_scripts': ['rofi-tpb = rofi_tpb.cli:main']}

setup_kwargs = {
    'name': 'rofi-tpb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
