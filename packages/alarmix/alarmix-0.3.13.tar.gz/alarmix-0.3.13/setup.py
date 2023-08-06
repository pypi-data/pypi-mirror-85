# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alarmix', 'alarmix.client', 'alarmix.daemon']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'prettytable>=1.0.1,<2.0.0', 'pydantic>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['alarmc = alarmix.client.main:main',
                     'alarmd = alarmix.daemon.main:main']}

setup_kwargs = {
    'name': 'alarmix',
    'version': '0.3.13',
    'description': 'Alarm manager server and client',
    'long_description': None,
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
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
