# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manufactory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'manufactory',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Michael Oliver',
    'author_email': 'contact@michaeloliver.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
