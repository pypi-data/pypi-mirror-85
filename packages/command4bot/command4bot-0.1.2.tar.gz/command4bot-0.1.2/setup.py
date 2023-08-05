# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['command4bot']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'command4bot',
    'version': '0.1.2',
    'description': 'A general purpose library for command-based iteraction made for bots',
    'long_description': '# Command For Bot\n\n![PyPI](https://img.shields.io/pypi/v/command4bot)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/command4bot)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/command4bot)\n\n![Run Tests](https://github.com/AllanChain/command4bot/workflows/Run%20Tests/badge.svg)\n[![codecov](https://codecov.io/gh/AllanChain/command4bot/branch/master/graph/badge.svg?token=RJV7MMZC5D)](https://codecov.io/gh/AllanChain/command4bot)\n\n![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/AllanChain/command4bot)\n![GitHub last commit](https://img.shields.io/github/last-commit/AllanChain/command4bot)\n\n![Check Code Style](https://github.com/AllanChain/command4bot/workflows/Check%20Code%20Style/badge.svg)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n:warning: The document is still working in progress!\n\n`command4bot` is a general purpose library for command-based iteraction made for bots, with command registry, command dependency (a.k.a. `setup`), ability to enable / disable commands, fallback functions included.\n\n- [Installation](#installation)\n- [Quick Start](#quick-start)\n- [Basic Concepts and Usage](#basic-concepts-and-usage)\n  - [Command](#command)\n  - [Setup (Command Dependency)](#setup-command-dependency)\n- [Todo](#todo)\n\n## Installation\n\n```shell\npip install command4bot\n```\n\n## Quick Start\n\n```python\nfrom command4bot import CommandsManager\n\nmgr = CommandsManager()\n\n@mgr.command\ndef greet(payload):\n    return f"Hello, {payload}!"\n\nmgr.exec(\'greet John\')  # \'Hello, John!\'\n```\n\n## Basic Concepts and Usage\n\n### Command\n\nCommand is a function taking a positional argument (`payload`) and optional keyword arguments.\n\n### Setup (Command Dependency)\n\nCommand dependencies is trivial to manage if the command is always open.\n\nFor example, setup web socket connection if any command needs, and close the connection if all commands need the socket are closed.\n\n```python\n@mgr.setup\ndef ws():\n    ws_client = WSClient(\'localhost:8888\')\n    yield ws_client\n    ws_client.close()\n\n@mgr.command\ndef send(paload, ws):\n    ws.send(payload)\n```\n\n\n## Todo\n\n- [ ] Support for commands need interaction\n',
    'author': 'Allan Chain',
    'author_email': 'allanchain@pku.edu.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AllanChain/command4bot',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
