# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slim',
 'slim.base',
 'slim.base.types',
 'slim.base.view',
 'slim.base.web',
 'slim.ext',
 'slim.ext.crud_view',
 'slim.ext.openapi',
 'slim.tools',
 'slim.tools.migrate',
 'slim.utils',
 'slim_cli',
 'slim_cli.template',
 'slim_cli.template.api',
 'slim_cli.template.api.validate',
 'slim_cli.template.model',
 'slim_cli.template.permissions',
 'slim_cli.template.permissions.roles',
 'slim_cli.template.permissions.tables',
 'slim_cli.template.tests',
 'slim_cli.template.tools']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.6',
 'click>=7.0,<8.0',
 'msgpack>=1.0.0,<2.0.0',
 'multidict>=4.5,<6.0',
 'pycurd>=0.1.16',
 'python-multipart>=0.0.5,<0.0.6',
 'typing_extensions>=3.6.5',
 'uvicorn>0.11.0,<0.13.0',
 'yarl>=1.0,<1.5']

entry_points = \
{'console_scripts': ['slim = slim_cli.main:cli']}

setup_kwargs = {
    'name': 'slim',
    'version': '0.7.0a7',
    'description': 'A Simple ASGI Web framework',
    'long_description': None,
    'author': 'fy',
    'author_email': 'fy0748@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fy0/slim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9',
}


setup(**setup_kwargs)
