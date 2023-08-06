# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torrentmirror']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'docopt>=0.6.2,<0.7.0',
 'pygogo>=0.13.2,<0.14.0',
 'robobrowser>=0.5.3,<0.6.0',
 'tabulate>=0.8.7,<0.9.0',
 'werkzeug==0.16.1',
 'xdg>=5.0.1,<6.0.0',
 'yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['torrentmirror = torrentmirror:main']}

setup_kwargs = {
    'name': 'torrentmirror',
    'version': '2.0.1',
    'description': 'TorrentMirror API and CLI interface',
    'long_description': '\\:tv\\: TorrentMirror CLI and python library\n=================================================\n\nPython library to expose torrentmirror as a command and python library.\n\n.. contents:: :local:\n\n\n\\:tv\\: torrentmirror - TorrentMirror CLI Interface\n------------------------------------------------------\n\nYou can invoke torrentmirror command to have a nice tabulated list of mirrors\nin your terminal\n\n.. image:: http://i.imgur.com/HdY0NIl.png\n\n\n\\:star\\: Usage\n++++++++++++++++\n\n::\n\n    TorrentMirror.\n\n        Usage: torrentmirror [<torrent_mirror_url>]\n\n\n\\:star\\: Installation\n---------------------\n\nThis is a python package available on pypi.\n\nWith python3.8 installed just execute\n\n.. code:: sh\n\n    pip3.8 install torrentmirror\n\n\nIf it asks about permissions and you don\'t know what to do, you should\nprobably read `Jamie Matthews\'s article about virtualenvs <https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/>`_\n\n\n\n\\:notebook\\: Library Usage\n---------------------------\n\nTorrentMirror exposes a simple get_proxies method\n\n\n.. code:: python\n\n        get_proxies(url="https://www.torrentmirror.net/", renew=False)\n\nIt returns a dict in the form\n\n.. code:: python \n\n        {\n          "site_name": [\n            {\n              "link": "http://foo.com",\n              "status": "ONLINE",\n              "percentage": 40\n            },\n            {\n              "link": "http://foo.com",\n              "status": "ONLINE",\n              "percentage": 40\n            }\n          ]\n        }\n',
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
