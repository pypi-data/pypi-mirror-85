# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapz',
 'mapz.methods',
 'mapz.modifiers',
 'mapz.tests',
 'mapz.tests.methods',
 'mapz.tests.modifiers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mapz',
    'version': '1.1.14',
    'description': 'Extension of dict features',
    'long_description': '# MapZ\n\n<h2>Extension of standard `dict` capabilities.</h2>\n\n<p>\n    <a href="https://github.com/ilexconf/mapz/actions"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/ilexconf/mapz/release?logo=github"></a>\n    <a href="https://codecov.io/gh/ilexconf/mapz/"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/ilexconf/mapz?logo=codecov"></a>\n    <a href="https://pypi.org/project/mapz/"><img alt="PyPI" src="https://img.shields.io/pypi/v/mapz?color=blue&logo=pypi"></a>\n</p>\n',
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': 'vduseev',
    'maintainer_email': 'vagiz@duseev.com',
    'url': 'https://github.com/ilexconf/mapz',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
