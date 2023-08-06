# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cornac',
 'cornac.core',
 'cornac.core.config',
 'cornac.core.schema',
 'cornac.iaas',
 'cornac.operator',
 'cornac.web',
 'cornac.web.cornac',
 'cornac.web.iam',
 'cornac.web.rds',
 'cornac.web.sts']

package_data = \
{'': ['*'], 'cornac': ['files/*']}

install_requires = \
['awscli-plugin-endpoint==0.4',
 'awscli==1.18.150',
 'bjoern>=2.2,<3.0',
 'botocore==1.18.9',
 'click>=7.0,<8.0',
 'dramatiq-pg>=0.6,<0.7',
 'dramatiq>=1.5,<2.0',
 'flask-cors>=3.0,<4.0',
 'flask-dramatiq>=0.5.0,<0.6.0',
 'flask-mailman==0.1.7',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask>=1.0,<2.0',
 'httpx>=0.13.3,<0.14.0',
 'periodiq>=0.11.0,<0.12.0',
 'python-dotenv>=0.10.1,<0.11.0',
 'python-etcd>=0.4.5,<0.5.0',
 'pyvmomi>=6.7,<7.0',
 'sqlalchemy-json>=0.2.3,<0.3.0',
 'tenacity>=6.0,<7.0']

entry_points = \
{'console_scripts': ['cornac = cornac.cli:entrypoint'],
 'cornac.operators': ['basic = cornac.operator.basic:BasicOperator',
                      'none = cornac.operator.none:NoneOperator']}

setup_kwargs = {
    'name': 'pgcornac',
    'version': '2.0.0',
    'description': 'RDS-compatible Managed-Postgres Webservice',
    'long_description': '# REST Service\n\nThe Cornac webservice is an open-source implementation of AWS RDS API enabling\nthe use of aws CLI to manage your Postgres instances.\n\n**⚠ This project is at its early stage of development. ⚠**\n\n\n## Features\n\n- Subset of RDS API compatible with awscli.\n- Configurable infastructure provider: libvirt, VMWare.\n\n\n## Installation\n\ncornac web service is available on PyPI as `pgCornac`. You need more than a `pip\ninstall` to such service. See [installation instructions](docs/install.md) for\ndetails.\n\n\n## Support\n\ncornac is build for you by Dalibo, the french leader in PostgreSQL support. Feel\nfree to [open an issue on GitHub\nproject](https://github.com/dalibo/cornac/issues/new) page.\n',
    'author': 'Étienne BERSAC',
    'author_email': 'etienne.bersac@dalibo.com',
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
