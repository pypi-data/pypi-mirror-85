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
    'version': '0.3.14',
    'description': 'Alarm manager server and client',
    'long_description': '<div align="center">\n    <img src="logo.png" alt="logo">\n    <p>CLI alarm manager based on unix sockets</p>\n</div>\n\n---\n\n```\npython -m pip install alarmix\n```\n\n## Usage\n⚠️ [MPV](https://mpv.io/) must be installed and accessible ⚠️\n1. Start alarmd daemon\n```bash\nalarmd --sound "path/to/sound"\n```\n\nThen you can manage your alarms with `alarmc` command.\n```bash\nalarmc # Show scheduled alarms\nalarmc stop # Stop buzzing alarm\nalarmc add 20:00 19:30 14:00 # Add alarms\nalarmc add 20:00 --delete # delete TODO: make other command\nalarmc\n\nalarmc -h # Show help\n```',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/alarmix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
