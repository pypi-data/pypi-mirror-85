# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_python_lib']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=21.5.0,<22.0.0']

setup_kwargs = {
    'name': 'ml-python-lib',
    'version': '0.0.2',
    'description': 'Machine Learning Library for tensorflow training algorithms',
    'long_description': None,
    'author': 'Tanguy Coatalem',
    'author_email': 'tanguy.coatalem@cogneed.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
