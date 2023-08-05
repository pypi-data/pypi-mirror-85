# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['capablerobot_usbregister']

package_data = \
{'': ['*'], 'capablerobot_usbregister': ['binaries/*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['usbregister = capablerobot_usbregister.main:console']}

setup_kwargs = {
    'name': 'capablerobot-usbregister',
    'version': '1.3.2',
    'description': 'Windows command line tool to assist in registering USB drivers',
    'long_description': "# Capable Robot : USB Register\n\nWindows command line tool & python library to assist in registering USB drivers.\n\nThis repository includes binaries built from the [libwdi](https://github.com/pbatard/libwdi) project.  Specifically:\n\n- `wdi-64bit.exe` : 64-bit binary of [wdi-simple](https://github.com/pbatard/libwdi/blob/master/examples/wdi-simple.c), version v1.3.1.\n- `wdi-32bit.exe` : 32-bit binary of [wdi-simple](https://github.com/pbatard/libwdi/blob/master/examples/wdi-simple.c), version v1.3.1.\n\nThe python wrapper automatically runs the appropiate binary based on your computers's architecture.\n\nThe wrapper also includes registration settings for the following products, enabling error-free device registration.\n\n- [Capable Robot Programmable USB Hub](https://capablerobot.com/products/programmable-usb-hub/)\n\n\nPull requests to add additional devices will be gladly accepted.\n\n## Installation\n\n```\n    pip install capablerobot_usbregister\n```\n\n## Usage\n\n```\n\n    Usage: usbregister [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --verbose  Increase logging level.\n      --help     Show this message and exit.\n\n    Commands:\n      list      Print the known devices which can be registered to drivers.\n      device    Register the specified device.\n      register  Registers driver based on Vendor ID, Product ID, and interface ID.\n\n```\n",
    'author': 'Chris Osterwood',
    'author_email': 'osterwood@capablerobot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CapableRobot/CapableRobot_USBRegister',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
