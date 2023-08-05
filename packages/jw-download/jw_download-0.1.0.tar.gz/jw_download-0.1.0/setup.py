# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jw_download']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'confuse>=1.3.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.51.0,<5.0.0',
 'yaspin>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['jw = jw_download.main:main']}

setup_kwargs = {
    'name': 'jw-download',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Unviray',
    'author_email': 'unviray@gmail.com',
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
