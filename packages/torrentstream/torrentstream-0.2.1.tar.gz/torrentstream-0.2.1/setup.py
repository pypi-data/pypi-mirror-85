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
    'version': '0.2.1',
    'description': "Quick n' dirty torrent streaming with libtorrent and python",
    'long_description': ".. image:: docs/tree.jpeg\n\nLibtorrent made easy\n--------------------\n\nThis is pythonic high-level libtorrent API, inspired on the for-humans trend\nset by Kenneth Reitz (https://github.com/not-kennethreitz).\n\nTorrentStream is centered around the principle of `streaming` a torrent\n(sequential download, buffering and playing).\n\n|pypi| |release| |downloads| |python_versions| |pypi_versions|\n\n.. |pypi| image:: https://img.shields.io/pypi/l/torrentstream\n.. |release| image:: https://img.shields.io/librariesio/release/pypi/torrentstream\n.. |downloads| image:: https://img.shields.io/pypi/dm/torrentstream\n.. |python_versions| image:: https://img.shields.io/pypi/pyversions/torrentstream\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/torrentstream\n\nTorrentStream exposes a CLI command, intended as an example usage.\n\n.. image:: docs/torrentstream_usage.png\n\n\nTorrent objects are context managers that can clean up torrent content after\nyou finish using them.\n\n*add_torrent* method of a TorrentSession returns a Torrent object, thus can be\nused directly as a context manager.\n\n.. code:: python\n\n    async def stream_torrent(hash_torrent):\n        session = TorrentSession()\n\n        # By default this will cleanup torrent contents after playing\n        with session.add_torrent(magnet_link=hash_torrent, remove_after=True) as torrent:\n            # Force sequential mode\n            torrent.sequential(True)\n\n            # Wait for torrent to be started\n            await torrent.wait_for('started')\n\n            # Get first match of a media file\n            try:\n                media = next(a for a in torrent\n                             if a.is_media and not 'sample' in a.path.lower())\n            except StopIteration:\n                raise Exception('Could not find a playable source')\n\n            with timeout(5 * 60):  # Abort if we can't fill 5% in 5 minutes\n                await media.wait_for_completion(5)\n\n            return await asyncio.gather(media.wait_for_completion(100),\n                                        media.launch())\n",
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
