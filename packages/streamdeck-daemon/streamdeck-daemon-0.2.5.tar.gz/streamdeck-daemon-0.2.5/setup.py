# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamdeck_daemon',
 'streamdeck_daemon.config',
 'streamdeck_daemon.handlers',
 'streamdeck_daemon.logging',
 'streamdeck_daemon.plugins']

package_data = \
{'': ['*']}

install_requires = \
['phue>=1.1,<2.0',
 'pillow>=7.2.0,<8.0.0',
 'pluginbase>=1.0.0,<2.0.0',
 'pyautogui>=0.9.51,<0.10.0',
 'pyyaml>=5.3.1,<6.0.0',
 'simpleobsws>=0.0.7,<0.0.8',
 'streamdeck>=0.8.2,<0.9.0',
 'xdg>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['streamdeck = '
                     'streamdeck_daemon.streamdeck:run_streamdeck']}

setup_kwargs = {
    'name': 'streamdeck-daemon',
    'version': '0.2.5',
    'description': 'A Simple daemon for controlling the Elgato Stremdeck devices',
    'long_description': None,
    'author': 'Jesper Fussing Mørk',
    'author_email': 'jfm@moerks.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
