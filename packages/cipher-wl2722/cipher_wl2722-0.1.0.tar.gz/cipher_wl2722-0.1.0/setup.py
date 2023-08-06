# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipher_wl2722']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cipher-wl2722',
    'version': '0.1.0',
    'description': 'Python package that contains the cipher function!',
    'long_description': None,
    'author': 'Wanyingli',
    'author_email': 'wl2722@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
