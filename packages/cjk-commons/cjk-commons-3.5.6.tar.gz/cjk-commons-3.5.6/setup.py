# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjk_commons']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0', 'appdirs>=1.4,<2.0', 'loguru>=0.5,<0.6', 'yodl>=1.0,<2.0']

setup_kwargs = {
    'name': 'cjk-commons',
    'version': '3.5.6',
    'description': 'Commons',
    'long_description': None,
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cujoko/commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
