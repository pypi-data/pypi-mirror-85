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
    'version': '0.1.1',
    'description': 'Salient: A simple SqlAlchemy Linter.',
    'long_description': '\n# Table of Contents\n\n1.  [Salient: A simple SQLAlchemy Linter](#org6332640)\n    1.  [What is it?](#orgd4c6bef)\n    2.  [Why?](#org962193d)\n    3.  [Simple and Naive](#org0461335)\n        1.  [The Benefits of Naivete](#orgc8fde2a)\n        2.  [Trade-Offs](#org6abd652)\n    4.  [The Name](#org8b43816)\n    5.  [Usage](#orgc7de55c)\n    6.  [Current State](#org1f4a428)\n    7.  [Requirements](#org26d16f8)\n    8.  [Contributing](#org1da3846)\n\n\n<a id="org6332640"></a>\n\n# Salient: A simple SQLAlchemy Linter\n\n\n<a id="orgd4c6bef"></a>\n\n## What is it?\n\nSalient is a rather simple, naive, even simplistic, linter for SQLAlchemy class based models.\n\n\n<a id="org962193d"></a>\n\n## Why?\n\nI wrote this after discovering that a SA model in a project I work on had a table column that was defined once and then redefined with a different definition later in the model. I have also found that unnecessary `nullable=True` and `index=False` can be found all over the place.  I wrote this after discovering that a SA model in a project I work on had a table column that was defined once and then redefined with a different definition later in the model. I have also found that unnecessary `nullable=True` and `index=False` can be found all over the place. \n\n\n<a id="org0461335"></a>\n\n## Simple and Naive\n\nSalient takes few options and parses SA models in a naive manner. Salient does not currently use an AST or a finite state machine to parse source code. Rather it parses like you might with grep.\n\n\n<a id="orgc8fde2a"></a>\n\n### The Benefits of Naivete\n\nSalient should be simple to understand and to maintain.\n\n\n<a id="org6abd652"></a>\n\n### Trade-Offs\n\nSalient assumes a Python module contains one SA class based model, so if you have a module with multiple classes and they have column names in common you would need to separate them or not check for redefined columns. This also means that if you have `nullable=True` in a module being linted outside of a column definition the linter is going to be most unhappy with you.\n\n\n<a id="org8b43816"></a>\n\n## The Name\n\nSalient comes from my abbreviating SQLAlchemy as SA and it being a linter, SAli[e]nt.\n\n\n<a id="orgc7de55c"></a>\n\n## Usage\n\nThe idea, and hope, is that your SA models live in their own directory separate from other source code. Salient probably won\'t break if it sees other source, but it was really intended to mostly look at SA models.\n\n`poetry run python salient.py -rni src/app/models/*.py`\n\n    1 file(s) with errors were found.\n    \n    examples/all_problems.py\n      Redefined Columns - unoriginal_column_name:\n        16: Column(Integer)\n        19: Column(Boolean)\n      Unnecessary nullable=True:\n        17:     col_1 = Column(nullable=True)\n      Unnecessary index=False:\n        18:     col_2 = Column(index=False)\n\nYou can run with the `-h` or `--help` parameter for more options.\n\n    usage: salient.py [-h] [-n] [-i] [-r] [--config CONFIG] [-R RECURSIVE] [-1 STOP_AFTER_FIRST_ERROR] files [files ...]\n    \n    positional arguments:\n      files                 files to lint\n    \n    optional arguments:\n      -h, --help            show this help message and exit\n      -n, --nullable-true   Check for unnecessary nullable=True\n      -i, --index-false     Check for unnecessary index=False\n      -r, --redefined-column\n                            Check for columns that are redefined.\n      --config CONFIG       Load options from CONFIG FILE.\n      -R, --recursive       If FILES includes directories scan those as well\n      -1 STOP_AFTER_FIRST_ERROR, --stop-after-first-error STOP_AFTER_FIRST_ERROR\n                            stop after first error\n\n\n<a id="org1f4a428"></a>\n\n## Current State\n\nAlpha / MVP\n\n-   Believed to do what it says on the tin, but YMMV\n-   Not all command line options are implemented. (help, and the three linting rules work, that is all)\n-   Doesn\'t recurse subdirectories\n-   Doesn\'t currently use a config file, and no environment variables have been implemented.\n-   Still has TODOs in the code. :)\n-   Mostly untested, but the most complex of the linters is tested.\n-   PRs welcome!\n\n\n<a id="org26d16f8"></a>\n\n## Requirements\n\n-   Python 3.8 or above.\n    -   I\'ve set the Poetry config to require Python 3.8 or above. I don\'t believe anything is preventing use with 3.7, but I am not opposed to throwing in a walrus here and there if it is the best way to do something.\n-   Poetry, any modern version.\n\n\n<a id="org1da3846"></a>\n\n## Contributing\n\n-   Code is formatted with the latest version of Black.\n-   MyPy isn\'t configured yet, but please use typehints. (Not everything is typehinted, but the project is a day old at the time of this writing!)\n-   New code should be tested.\n\n',
    'author': 'Tom Faulkner',
    'author_email': 'faulkner@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomFaulkner/sa_lint',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
