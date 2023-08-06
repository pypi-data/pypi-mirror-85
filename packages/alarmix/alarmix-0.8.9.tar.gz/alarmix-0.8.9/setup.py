# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alarmix', 'alarmix.client', 'alarmix.daemon']

package_data = \
{'': ['*']}

install_requires = \
['daemonize>=2.5.0,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'prettytable>=2.0.0,<3.0.0',
 'pydantic>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['alarmc = alarmix.client.main:main',
                     'alarmd = alarmix.daemon.main:main']}

setup_kwargs = {
    'name': 'alarmix',
    'version': '0.8.9',
    'description': 'Alarm manager server and client',
    'long_description': '|py_versions| |build_statuses| |pypi_versions|\n\n.. |py_versions| image:: https://img.shields.io/pypi/pyversions/alarmix?style=flat-square\n    :alt: python versions\n\n.. |build_statuses| image:: https://img.shields.io/github/workflow/status/s3rius/alarmix/Release%20python%20package?style=flat-square\n    :alt: build status\n\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/alarmix?style=flat-square\n    :alt: pypi version\n    :target: https://pypi.org/project/alarmix/\n\n.. image:: https://raw.githubusercontent.com/s3rius/alarmix/master/logo.png\n    :alt: logo\n    :align: center\n\n===============\nInstallation\n===============\n\n.. code-block:: bash\n\n    python -m pip install alarmix\n\n⚠️ `MPV <https://mpv.io/>`_ must be installed and accessible ⚠️\n\nAt first, you need to start alarmd daemon:\n\n.. code-block:: bash\n\n    # Run alarmd-server as a daemon\n    alarmd -s "path/to/sound/to/play" -d\n\n    # To kill it you need to run\n    alarmd kill\n\n    # Of course you can see help\n    alarmd -h\n\nThen you can manage your alarms with `alarmc` command.\n\n.. code-block:: bash\n\n    alarmc # Show scheduled alarms for today\n    alarmc -f # Show all scheduled alarms\n    alarmc stop # Stop buzzing alarm\n    alarmc add 20:00 19:30 14:00 # Add alarms\n    alarmc add +30 +2:40 # Add alarms with relative time\n    alarmc delete 20:00 # Remove alarm from schedule\n    alarmc\n\n    alarmc -h # Show help\n\nAlso alarmc can display information about your schedule in different formats:\n\n.. code-block::\n\n    ➜  ~ alarmc # Default schedule information\n    +------------+----------------+\n    | alarm time | remaining time |\n    +------------+----------------+\n    |  09:30:00  |    9:01:28     |\n    +------------+----------------+\n\n    ➜  ~ alarmc -r # Raw data without table formatting (separated by \'\\t\' character)\n    alarm time      remaining time\n    09:30:00        9:00:43\n\n    ➜  ~ alarmc -w # Show "When" column\n    +------------+----------------+----------+\n    | alarm time | remaining time |   when   |\n    +------------+----------------+----------+\n    |  09:30:00  |    8:58:58     | weekdays |\n    +------------+----------------+----------+\n\n    ➜  ~ alarmc -c # Show "Cancelled" column\n    +------------+----------------+-----------+\n    | alarm time | remaining time | cancelled |\n    +------------+----------------+-----------+\n    |  09:30:00  |    8:57:35     |   False   |\n    +------------+----------------+-----------+\n\n    # All options can be combined\n    ➜  ~ alarmc -rwc\n    alarm time      remaining time  when            cancelled\n    09:30:00        8:58:15         weekdays        False\n\n',
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
