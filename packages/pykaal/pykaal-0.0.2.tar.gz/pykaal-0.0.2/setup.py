# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pykaal']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.3.0', 'numpy==1.19.1']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'pykaal',
    'version': '0.0.2',
    'description': 'Fluorescence time analysis',
    'long_description': None,
    'author': 'Sarthak Jariwala',
    'author_email': 'jariwala@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
