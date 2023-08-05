# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['p5core']

package_data = \
{'': ['*']}

install_requires = \
['py7zr>=0.11.0,<0.12.0',
 'requests>=2.20.0,<3.0.0',
 'simplelogging>=0.10,<0.12']

entry_points = \
{'console_scripts': ['p5 = p5core.install:install']}

setup_kwargs = {
    'name': 'p5core',
    'version': '0.3.0',
    'description': 'Programmer en Python comme un Pro Par la Pratique',
    'long_description': '# p5core\n\n[![PyPI](https://img.shields.io/pypi/v/p5core.svg)](https://pypi.python.org/pypi/p5core)\n[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Downloads](https://pepy.tech/badge/p5core)](https://pepy.tech/project/p5core)\n\np⁵\xa0: Programmer en Python comme un Pro Par la Pratique\n\n## License\n\nCopyright Vincent Poulailleau 2020\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/p5',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
