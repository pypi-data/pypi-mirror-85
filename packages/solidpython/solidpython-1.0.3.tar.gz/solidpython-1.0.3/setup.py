# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['solid', 'solid.examples', 'solid.examples.mazebox', 'solid.test']

package_data = \
{'': ['*'],
 'solid': ['mypy/mypy_test.py'],
 'solid.test': ['solidpython.egg-info/*']}

install_requires = \
['PrettyTable==0.7.2',
 'euclid3>=0.1.0,<0.2.0',
 'pypng>=0.0.19,<0.0.20',
 'regex>=2019.4,<2020.0']

setup_kwargs = {
    'name': 'solidpython',
    'version': '1.0.3',
    'description': 'Python interface to the OpenSCAD declarative geometry language',
    'long_description': None,
    'author': 'Evan Jones',
    'author_email': 'evan_t_jones@mac.com',
    'url': 'https://github.com/SolidCode/SolidPython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
