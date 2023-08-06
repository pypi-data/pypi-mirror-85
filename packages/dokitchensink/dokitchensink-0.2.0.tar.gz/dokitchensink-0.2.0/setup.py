# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dokitchensink']

package_data = \
{'': ['*']}

install_requires = \
['python-digitalocean>=1.15.0,<2.0.0']

entry_points = \
{'console_scripts': ['dokitchensink-drain = dokitchensink.cli_interface:drain',
                     'dokitchensink-faucet = '
                     'dokitchensink.cli_interface:faucet']}

setup_kwargs = {
    'name': 'dokitchensink',
    'version': '0.2.0',
    'description': 'Thin wrapper for python-digitalocean, mostly to automate DNS record creation after droplet creation',
    'long_description': None,
    'author': 'Aljoscha Vollmerhaus',
    'author_email': 'git@aljoscha.vollmerhaus.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avollmerhaus/dokitchensink',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
