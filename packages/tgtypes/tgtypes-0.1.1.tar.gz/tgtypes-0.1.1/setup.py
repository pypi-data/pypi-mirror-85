# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgtypes',
 'tgtypes.descriptors',
 'tgtypes.identities',
 'tgtypes.interfaces',
 'tgtypes.persistence',
 'tgtypes.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'tgtypes',
    'version': '0.1.1',
    'description': 'Unified Python models for Telegram Messenger.',
    'long_description': '# tgtypes\n\nLibrary-agnostic Python models for Telegram types.\n\nUsed by [botkit](https://github.com/autogram/botkit).\n',
    'author': 'JosXa',
    'author_email': 'joscha.goetzer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JosXa/tgintegration',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
