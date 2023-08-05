# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_commit', 'auto_commit.cli', 'auto_commit.core']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['auto-commit = auto_commit.__main__:run']}

setup_kwargs = {
    'name': 'auto-commit',
    'version': '0.1.0',
    'description': 'Make automatically git commits when coding',
    'long_description': None,
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
