# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.googleads']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.0.8,<2.0.0', 'backoff==1.10.0', 'google-ads>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'arcane-googleads',
    'version': '1.0.3',
    'description': 'Package description',
    'long_description': '# Arcane google-ads\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
