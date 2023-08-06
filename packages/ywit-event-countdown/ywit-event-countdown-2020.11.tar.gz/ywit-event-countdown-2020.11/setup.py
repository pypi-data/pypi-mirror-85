# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'ywit_event_countdown']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['ywit-countdown = ywit_event_countdown.cli:main']}

setup_kwargs = {
    'name': 'ywit-event-countdown',
    'version': '2020.11',
    'description': "This library and application will tell you how long until NetAp's next YWIT event",
    'long_description': '# Using GitHub for CI/CD\n\nThis repository is meant to accompany the "Using GitHub for CI/CD" workshop from\nthe NetApp YWIT 2020 event: https://netapp.ywit.io/workshops/ci_cd_with_github\n\nContained here is a simple Python package and a set of simple GitHub actions which\nallow for automation of the testing, building, and release of a Python package.\n\nThe techniques shown in the workshop are not unique to a Python package but can\nbe applied to any project you might create and store in GitHub.\n',
    'author': 'NetApp',
    'author_email': 'ng-ywit-questions@netapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NetApp-YWIT/ywit_2020_ci_cd_workshop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
