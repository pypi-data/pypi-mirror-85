# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobile_payments']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9.9,<4.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'mobile-payments',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Innocent Zenda',
    'author_email': 'zendainnocent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
