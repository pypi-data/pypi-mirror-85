# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openbayes_serving', 'openbayes_serving.debug', 'openbayes_serving.utils']

package_data = \
{'': ['*'], 'openbayes_serving.debug': ['static/*']}

install_requires = \
['flask>=1.1.1,<2.0.0',
 'httptools>=0.1.1,<0.2.0',
 'msgpack>=0.6.2,<0.7.0',
 'pprintpp>=0.4.0,<0.5.0',
 'requests>=2.24.0,<3.0.0',
 'uvicorn>=0.12.2,<0.13.0',
 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'openbayes-serving',
    'version': '0.1.9',
    'description': 'Framework for Openbayes Serving',
    'long_description': None,
    'author': 'Proton',
    'author_email': 'bwang@openbayes.com',
    'maintainer': 'Proton',
    'maintainer_email': 'bwang@openbayes.com',
    'url': 'https://openbayes.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
