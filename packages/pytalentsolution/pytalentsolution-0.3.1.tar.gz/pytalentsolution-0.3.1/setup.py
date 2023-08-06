# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytalentsolution']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.43.0,<0.44.0',
 'autoname>=0.1.2,<0.2.0',
 'google-cloud-talent>=2.0.0,<3.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'pytalentsolution',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
