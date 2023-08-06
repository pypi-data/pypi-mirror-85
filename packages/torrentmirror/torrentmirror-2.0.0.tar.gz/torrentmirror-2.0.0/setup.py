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
    'version': '2.0.0',
    'description': '',
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
