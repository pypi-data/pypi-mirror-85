# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timing_asgi', 'timing_asgi.integrations']

package_data = \
{'': ['*']}

install_requires = \
['alog>=0.9.13,<0.10.0']

setup_kwargs = {
    'name': 'timing-asgi',
    'version': '0.2.1',
    'description': 'ASGI middleware to emit timing metrics with something like statsd',
    'long_description': None,
    'author': 'Steinn Eldjárn Sigurðarson',
    'author_email': 'steinnes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
