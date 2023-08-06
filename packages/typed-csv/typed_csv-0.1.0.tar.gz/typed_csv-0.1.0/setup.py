# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_csv']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'typed-csv',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kesha1225',
    'author_email': 'samedov03@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
