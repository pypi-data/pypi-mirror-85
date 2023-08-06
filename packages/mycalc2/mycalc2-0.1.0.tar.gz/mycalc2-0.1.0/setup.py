# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mycalc2', 'mycalc2.models', 'mycalc2.utils', 'mycalc2.utils.extra']

package_data = \
{'': ['*']}

install_requires = \
['coverage[toml]>=5.3,<6.0', 'numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'mycalc2',
    'version': '0.1.0',
    'description': 'A simple calc library',
    'long_description': 'This is a simple Repo\n\n[![Tests](https://github.com/s4sarath/mycalc2/workflows/Tests/badge.svg)](https://github.com/s4sarath/mycalc2/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/s4sarath/mycalc2/branch/main/graph/badge.svg)](https://codecov.io/gh/s4sarath/mycalc2)\n',
    'author': 's4sarath',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s4sarath/mycalc2',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
