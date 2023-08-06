# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mboot2', 'mboot2.connection']

package_data = \
{'': ['*']}

install_requires = \
['bincopy==17.9.0',
 'click==7.0',
 'easy_enum==0.3.0',
 'fido2==0.8.1',
 'pyserial==3.4']

entry_points = \
{'console_scripts': ['mboot = mboot2.__main__:main']}

setup_kwargs = {
    'name': 'mboot2',
    'version': '0.3.4',
    'description': 'Python tool and library for interacting with NXP MCUBoot devices.',
    'long_description': None,
    'author': 'Martin Olejar,',
    'author_email': 'martin.olejar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/conorpp/pyMBoot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
