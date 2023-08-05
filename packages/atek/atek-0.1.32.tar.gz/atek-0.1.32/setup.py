# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atek']

package_data = \
{'': ['*']}

install_requires = \
['censusdata>=1.8,<2.0',
 'cytoolz>=0.10.1,<0.11.0',
 'jupyter>=1.0.0,<2.0.0',
 'openpyxl>=3.0.5,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pydantic[dotenv]>=1.7.2,<2.0.0',
 'pydomo>=0.2.3,<0.3.0',
 'pymysql>=0.10.0,<0.11.0',
 'requests>=2.24.0,<3.0.0',
 'sshtunnel>=0.1.5,<0.2.0',
 'tabulate>=0.8.7,<0.9.0',
 'toolz>=0.11.1,<0.12.0',
 'us>=2.0.2,<3.0.0',
 'xlrd>=1.2.0,<2.0.0',
 'xlsxwriter>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'atek',
    'version': '0.1.32',
    'description': '',
    'long_description': None,
    'author': 'JediHero',
    'author_email': 'hansen.rusty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
