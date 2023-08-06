# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbbdl']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'lxml>=4.6.1,<5.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['bbbdl = bbbdl.__main__:main']}

setup_kwargs = {
    'name': 'bbbdl',
    'version': '1.3.0',
    'description': 'A downloader for BigBlueButton meetings',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
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
