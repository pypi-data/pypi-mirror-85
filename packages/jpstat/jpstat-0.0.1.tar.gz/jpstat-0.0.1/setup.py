# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jpstat', 'jpstat.estat', 'jpstat.estat.util']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.2,<2.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'jpstat',
    'version': '0.0.1',
    'description': 'A library for accessing official statistics of Japan.',
    'long_description': '',
    'author': 'Xuanli Zhu',
    'author_email': 'akaguro.koyomi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alalalalaki/jpstat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
