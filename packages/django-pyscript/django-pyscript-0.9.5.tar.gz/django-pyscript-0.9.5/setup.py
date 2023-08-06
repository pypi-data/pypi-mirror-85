# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djpyscript']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-pyscript',
    'version': '0.9.5',
    'description': 'This package aims to provide a django file field that can store .py files and executes them.',
    'long_description': None,
    'author': 'Christopher Wittlinger',
    'author_email': 'c.wittlinger@intellineers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
