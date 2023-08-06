# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nkit', 'nkit.storage']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0',
 'dataset>=1.3.2,<2.0.0',
 'httpx>=0.16.1,<0.17.0',
 'pydantic>=1.7.2,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nkit = nkit.main:app']}

setup_kwargs = {
    'name': 'nkit',
    'version': '0.1.2',
    'description': '',
    'long_description': '# nkit V0.1\nHold Tight\n',
    'author': 'Ankit',
    'author_email': 'ankitsaini100205@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
