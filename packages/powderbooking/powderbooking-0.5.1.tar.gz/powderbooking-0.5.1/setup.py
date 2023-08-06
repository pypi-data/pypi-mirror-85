# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powderbooking']

package_data = \
{'': ['*']}

install_requires = \
['SQLalchemy>=1.3.19,<2.0.0']

setup_kwargs = {
    'name': 'powderbooking',
    'version': '0.5.1',
    'description': 'RESTful API backend for the Powderbooking application',
    'long_description': None,
    'author': 'Michael Kemna',
    'author_email': 'michael.kemna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
