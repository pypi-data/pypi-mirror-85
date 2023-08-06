# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdcclient',
 'sdcclient.monitor',
 'sdcclient.monitor.dashboard_converters',
 'sdcclient.secure']

package_data = \
{'': ['*']}

install_requires = \
['pyaml>=20.4.0,<21.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.23,<3.0',
 'urllib3>=1.25.8,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['tatsu>=4.4.0,<5.0.0'],
 ':python_version >= "3.8" and python_version < "4.0"': ['tatsu>=5.5.0,<6.0.0']}

setup_kwargs = {
    'name': 'sdcclient',
    'version': '0.14.4',
    'description': 'Python client for Sysdig Platform',
    'long_description': None,
    'author': 'Sysdig Inc.',
    'author_email': 'info@sysdig.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
