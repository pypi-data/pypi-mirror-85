# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic_io']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

extras_require = \
{'test': ['pytest>=6.1.2,<7.0.0',
          'pytest-cov>=2.10.1,<3.0.0',
          'tox>=3.20.1,<4.0.0',
          'flake8>=3.8.4,<4.0.0']}

entry_points = \
{'console_scripts': ['platonic-io = platonic-io.cli:main']}

setup_kwargs = {
    'name': 'platonic-io',
    'version': '0.1.0',
    'description': 'Package for recognizing registration plates',
    'long_description': None,
    'author': 'Szymon Cader',
    'author_email': 'szymon.sc.cader@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
