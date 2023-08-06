# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alarmix', 'alarmix.client', 'alarmix.daemon']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'prettytable>=2.0.0,<3.0.0', 'pydantic>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['alarmc = alarmix.client.main:main',
                     'alarmd = alarmix.daemon.main:main']}

setup_kwargs = {
    'name': 'alarmix',
    'version': '0.5.1',
    'description': 'Alarm manager server and client',
    'long_description': '.. image:: ./logo.png\n    :alt: logo\n    :align: center\n\n===============\nInstallation\n===============\n\n.. code-block:: bash\n\n    python -m pip install alarmix\n\n⚠️ `MPV <https://mpv.io/>`_ must be installed and accessible ⚠️\n\nAt first, you need to start alarmd daemon:\n\n.. code-block:: bash\n\n    alarmd --sound "path/to/sound"\n\nThen you can manage your alarms with `alarmc` command.\n\n.. code-block:: bash\n\n    alarmc # Show scheduled alarms for today\n    alarmc -f # Show all scheduled alarms\n    alarmc stop # Stop buzzing alarm\n    alarmc add 20:00 19:30 14:00 # Add alarms\n    alarmc add +30 +2:40 # Add alarms with relative time\n    alarmc delete 20:00 # Remove alarm from schedule\n    alarmc\n\n    alarmc -h # Show help\n',
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
