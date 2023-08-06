# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipher_sd3329']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cipher-sd3329',
    'version': '0.1.0',
    'description': "The package is used to encrypt or decrypt text via Caesar's cipher.",
    'long_description': None,
    'author': 'Siyu',
    'author_email': 'sd3329@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
