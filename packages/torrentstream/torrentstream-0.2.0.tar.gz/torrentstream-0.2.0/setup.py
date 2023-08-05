# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torrentstream']

package_data = \
{'': ['*']}

install_requires = \
['async_timeout>=3.0.1,<4.0.0', 'rich>=9.2.0,<10.0.0']

entry_points = \
{'console_scripts': ['torrentstream = torrentstream:main']}

setup_kwargs = {
    'name': 'torrentstream',
    'version': '0.2.0',
    'description': "Quick n' dirty torrent streaming with libtorrent and python",
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
