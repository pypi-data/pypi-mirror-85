# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gvm',
 'gvm.protocols',
 'gvm.protocols.gmpv208',
 'gvm.protocols.gmpv214',
 'gvm.protocols.gmpv7',
 'gvm.protocols.gmpv8',
 'gvm.protocols.gmpv9',
 'tests',
 'tests.connections',
 'tests.protocols',
 'tests.protocols.gmp',
 'tests.protocols.gmpv208',
 'tests.protocols.gmpv208.testcmds',
 'tests.protocols.gmpv208.testtypes',
 'tests.protocols.gmpv214',
 'tests.protocols.gmpv214.testcmds',
 'tests.protocols.gmpv214.testtypes',
 'tests.protocols.gmpv7',
 'tests.protocols.gmpv7.testcmds',
 'tests.protocols.gmpv7.testtypes',
 'tests.protocols.gmpv8',
 'tests.protocols.gmpv8.testcmds',
 'tests.protocols.gmpv8.testtypes',
 'tests.protocols.gmpv9',
 'tests.protocols.gmpv9.testcmds',
 'tests.protocols.gmpv9.testtypes',
 'tests.protocols.osp',
 'tests.transforms',
 'tests.utils',
 'tests.xml']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.6.0,<0.7.0', 'lxml>=4.5.0,<5.0.0', 'paramiko>=2.7.1,<3.0.0']

setup_kwargs = {
    'name': 'python-gvm',
    'version': '20.11.2',
    'description': 'Library to communicate with remote servers over GMP or OSP',
    'long_description': "![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)\n\n# Greenbone Vulnerability Management Python Library <!-- omit in toc -->\n\n[![GitHub releases](https://img.shields.io/github/release-pre/greenbone/python-gvm.svg)](https://github.com/greenbone/python-gvm/releases)\n[![PyPI release](https://img.shields.io/pypi/v/python-gvm.svg)](https://pypi.org/project/python-gvm/)\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/greenbone/python-gvm/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/greenbone/python-gvm/?branch=master)\n[![code test coverage](https://codecov.io/gh/greenbone/python-gvm/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbone/python-gvm)\n[![CircleCI](https://circleci.com/gh/greenbone/python-gvm/tree/master.svg?style=svg)](https://circleci.com/gh/greenbone/python-gvm/tree/master)\n\nThe Greenbone Vulnerability Management Python API library (**python-gvm**) is a\ncollection of APIs that help with remote controlling a Greenbone Security\nManager (GSM) appliance and its underlying Greenbone Vulnerability Manager\n(GVM). The library essentially abstracts accessing the communication protocols\nGreenbone Management Protocol (GMP) and Open Scanner Protocol (OSP).\n\n## Table of Contents <!-- omit in toc -->\n\n- [Documentation](#documentation)\n- [Installation](#installation)\n  - [Requirements](#requirements)\n  - [Install using pip](#install-using-pip)\n- [Example](#example)\n- [Support](#support)\n- [Maintainer](#maintainer)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Documentation\n\nThe documentation for python-gvm can be found at\n[https://python-gvm.readthedocs.io/](https://python-gvm.readthedocs.io/en/latest/).\nPlease always take a look at the documentation for further details. This\n**README** just gives you a short overview.\n\n## Installation\n\n### Version\n\nPlease consider to always use the **newest** version of `gvm-tools` and `python-gvm`.\nWe freqently update this projects to add features and keep them free from bugs.\nThis is why installing `python-gvm` using pip is recommended.\n\nThe current release of `python-gvm` can be used with all supported GOS versions.\n\n### Requirements\n\nPython 3.5 and later is supported.\n\n### Install using pip\n\npip 19.0 or later is required.\n\nYou can install the latest stable release of python-gvm from the Python Package\nIndex using [pip](https://pip.pypa.io/):\n\n    python3 -m pip install --user python-gvm\n\n## Example\n\n```python3\nfrom gvm.connections import UnixSocketConnection\nfrom gvm.protocols.gmp import Gmp\nfrom gvm.transforms import EtreeTransform\nfrom gvm.xml import pretty_print\n\nconnection = UnixSocketConnection()\ntransform = EtreeTransform()\n\nwith Gmp(connection, transform=transform) as gmp:\n    # Retrieve GMP version supported by the remote daemon\n    version = gmp.get_version()\n\n    # Prints the XML in beautiful form\n    pretty_print(version)\n\n    # Login\n    gmp.authenticate('foo', 'bar')\n\n    # Retrieve all tasks\n    tasks = gmp.get_tasks()\n\n    # Get names of tasks\n    task_names = tasks.xpath('task/name/text()')\n    pretty_print(task_names)\n```\n\n## Support\n\nFor any question on the usage of python-gvm please use the\n[Greenbone Community Portal](https://community.greenbone.net/c/gmp). If you\nfound a problem with the software, please\n[create an issue](https://github.com/greenbone/gvm-tools/issues)\non GitHub.\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/greenbone/python-gvm/pulls) on GitHub.\nFor bigger changes, please discuss it first in the\n[issues](https://github.com/greenbone/python-gvm/issues).\n\nFor development you should use [poetry](https://python-poetry.org)\nto keep you python packages separated in different environments. First install\npoetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of python-gvm (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nThe python-gvm repository uses [autohooks](https://github.com/greenbone/autohooks)\nto apply linting and auto formatting via git hooks. Please ensure the git hooks\nare active.\n\n    $ poetry install\n    $ poetry run autohooks activate --force\n\n## License\n\nCopyright (C) 2017-2020 [Greenbone Networks GmbH](https://www.greenbone.net/)\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).\n",
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greenbone/python-gvm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5.2,<4.0.0',
}


setup(**setup_kwargs)
