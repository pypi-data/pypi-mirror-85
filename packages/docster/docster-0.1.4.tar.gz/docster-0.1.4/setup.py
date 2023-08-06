# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docster']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'docstring-parser>=0.7.3,<0.8.0',
 'gitpython>=3.1.8,<4.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['docster = docster.main:app']}

setup_kwargs = {
    'name': 'docster',
    'version': '0.1.4',
    'description': 'Automatically extract your python docstrings into arbitrary Jinja2 templates',
    'long_description': '\n[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/BujarMurati/docster)\n\n# docster\nDocster is a static analysis tool that extracts doc strings from your code and inserts them into any Jinja2 template of your liking.\nUse this tool to automatically build documentation for your project.\nBecause docster performs static analysis instead of importing your modules, it is safe to use on modules whose import could cause side effects.\n\n',
    'author': 'BujarMurati',
    'author_email': '39311213+BujarMurati@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bujarmurati.github.io/docster/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
