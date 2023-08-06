# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dddpy']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=4.16.0,<5.0.0', 'Inject>=4.3.1,<5.0.0', 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'dddpy',
    'version': '0.0.1',
    'description': 'A framework to support ddd python projects',
    'long_description': None,
    'author': 'Yuichiro Smith',
    'author_email': 'contact@yu-smith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
