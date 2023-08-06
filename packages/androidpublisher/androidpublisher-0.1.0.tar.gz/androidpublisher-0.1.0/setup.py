# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['androidpublisher']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.12.5,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['rick-portal-gun = androidpublisher.main:app']}

setup_kwargs = {
    'name': 'androidpublisher',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Android Publisher\n',
    'author': 'leynier',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
