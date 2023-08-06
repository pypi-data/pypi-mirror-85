# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_fetcher_ops', 'dbnomics_fetcher_ops.commands']

package_data = \
{'': ['*']}

install_requires = \
['daiquiri>=2.1.1,<3.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'python-gitlab>=2.4.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'typer>=0.3.1,<0.4.0',
 'validators>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['dbnomics-fetchers = dbnomics_fetcher_ops.cli:main']}

setup_kwargs = {
    'name': 'dbnomics-fetcher-ops',
    'version': '0.1.5',
    'description': 'Manage DBnomics fetchers',
    'long_description': None,
    'author': 'Christophe Benz',
    'author_email': 'christophe.benz@cepremap.org',
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
