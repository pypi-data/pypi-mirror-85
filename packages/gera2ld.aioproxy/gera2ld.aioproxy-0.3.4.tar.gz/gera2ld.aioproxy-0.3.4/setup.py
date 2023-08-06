# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gera2ld', 'gera2ld.aioproxy', 'gera2ld.aioproxy.handlers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'gera2ld.socks>=0.4.3,<0.5.0',
 'importlib_metadata>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['aioproxy = gera2ld.aioproxy.cli:main']}

setup_kwargs = {
    'name': 'gera2ld.aioproxy',
    'version': '0.3.4',
    'description': '',
    'long_description': '# gera2ld.aioproxy\n\n[![PyPI](https://img.shields.io/pypi/v/gera2ld.aioproxy.svg)](https://pypi.org/project/gera2ld.aioproxy/)\n\nA simple transparent proxy server implemented with pure Python.\n\nBoth HTTP proxy and SOCKS proxy are supported on the same port.\n\n## Installation\n\n```sh\n$ pip3 install gera2ld.aioproxy\n```\n\n## Usage\n\n```sh\n$ aioproxy [-b :1086] [-x socks5://127.0.0.1:1080]\n```\n',
    'author': 'Gerald',
    'author_email': 'gera2ld@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/aioproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
