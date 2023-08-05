# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mentaws']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'boto3>=1.14.20,<2.0.0',
 'cryptography>=2.9.2,<3.0.0',
 'keyring>=21.4.0,<22.0.0']

entry_points = \
{'console_scripts': ['mentaws = mentaws.main:main', 'mts = mentaws.main:main']}

setup_kwargs = {
    'name': 'mentaws',
    'version': '0.5.2',
    'description': 'moMENTary AWS credentials',
    'long_description': None,
    'author': 'keithrozario',
    'author_email': 'keith@keithrozario.com',
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
