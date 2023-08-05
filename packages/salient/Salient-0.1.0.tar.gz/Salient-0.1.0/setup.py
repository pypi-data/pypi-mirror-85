# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['salient']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['salient = salient.salient:cmd']}

setup_kwargs = {
    'name': 'salient',
    'version': '0.1.0',
    'description': 'Salient: A simple SqlAlchemy Linter.',
    'long_description': None,
    'author': 'Tom Faulkner',
    'author_email': 'faulkner@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
