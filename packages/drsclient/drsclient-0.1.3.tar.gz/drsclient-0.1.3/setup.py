# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drsclient']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'backoff>=1.10.0,<2.0.0',
 'httpx>=0.15,<0.16',
 'jsonschema==2.5.1',
 'requests>=2.23.0,<3.0.0',
 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'drsclient',
    'version': '0.1.3',
    'description': 'GA4GH DRS Client',
    'long_description': None,
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
