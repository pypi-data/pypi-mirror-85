# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpa']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pandas>=1.1.4,<2.0.0', 'scipy>=1.5.4,<2.0.0']

setup_kwargs = {
    'name': 'xpa',
    'version': '0.1.0',
    'description': 'X-ray diffraction lib for analysis',
    'long_description': None,
    'author': 'Andre da Silva',
    'author_email': 'andrezio@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
