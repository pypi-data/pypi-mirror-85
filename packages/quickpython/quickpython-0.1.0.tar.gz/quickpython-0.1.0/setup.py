# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickpython', 'quickpython.examples']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'colorama>=0.4.4,<0.5.0',
 'ipdb>=0.13.4,<0.14.0',
 'isort>=5.4.2,<6.0.0',
 'prompt-toolkit>=3.0.6,<4.0.0',
 'pyfiglet>=0.8.post1,<0.9']

entry_points = \
{'console_scripts': ['qpython = quickpython.cli:start',
                     'quickpython = quickpython.cli:start']}

setup_kwargs = {
    'name': 'quickpython',
    'version': '0.1.0',
    'description': 'A retro interactive coding environment powered by Python and nostalgia ',
    'long_description': 'quickpython\n_________________\n\n[![PyPI version](https://badge.fury.io/py/quickpython.svg)](http://badge.fury.io/py/quickpython)\n[![Build Status](https://travis-ci.org/timothycrosley/quickpython.svg?branch=master)](https://travis-ci.org/timothycrosley/quickpython)\n[![codecov](https://codecov.io/gh/timothycrosley/quickpython/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/quickpython)\n[![Join the chat at https://gitter.im/timothycrosley/quickpython](https://badges.gitter.im/timothycrosley/quickpython.svg)](https://gitter.im/timothycrosley/quickpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/quickpython/)\n[![Downloads](https://pepy.tech/badge/quickpython)](https://pepy.tech/project/quickpython)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/quickpython/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/quickpython/)\n_________________\n\n**quickpython** A retro interactive coding environment powered by Python and nostalgia \n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
