# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_server']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'click>=7.0,<8.0',
 'gera2ld-pyserve>=0.3.1,<0.4.0',
 'importlib_metadata>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['json-server = json_server.cli:main']}

setup_kwargs = {
    'name': 'json-server.py',
    'version': '0.1.9',
    'description': 'A simple JSON server',
    'long_description': '# json-server.py\n\n[![PyPI](https://img.shields.io/pypi/v/json-server.py.svg)](https://pypi.org/project/json-server.py/)\n\nFake REST API with zero coding.\n\nThis project is heavily inspired by [json-server](https://github.com/typicode/json-server) in JavaScript.\n\nRequires Python 3.6+.\n\n## Installation\n\nIt\'s highly recommended to install with [pipx](https://pipxproject.github.io/pipx/).\n\n```sh\n$ pipx install json-server.py\n```\n\nOr install with pip at your own risk:\n\n```sh\n$ pip3 install json-server.py\n```\n\n## Get Started\n\nCreate a `db.json` file with following content:\n\n```json\n{\n  "posts": []\n}\n```\n\nStart a server:\n\n```sh\n$ json-server db.json\n```\n\nCreate a post:\n\n```sh\n$ curl -H \'content-type: application/json\' -d \'{"content":"blablabla"}\' http://localhost:3000/posts\n```\n\nList all posts:\n\n```sh\n$ curl http://localhost:3000/posts\n```\n\n## Usage\n\n```\nUsage: json-server [OPTIONS] [FILENAME]\n\n  Start a JSON server.\n\n  FILENAME refers to the JSON file where your data is stored. `db.json` will\n  be used if not specified.\n\nOptions:\n  --version        Show the version and exit.\n  -b, --bind TEXT  Set address to bind, default as `:3000`\n  --help           Show this message and exit.\n```\n\n**Note:**\n\n- Collections must be contained in your data file before starting the server, otherwise the server cannot decide the type of resources.\n\n### Examples\n\n```sh\n# Start with default config\n$ json-server\n\n# Listen on port 3000\n$ json-server -b :3000\n\n# Specify a json file\n$ json-server db.json\n```\n',
    'author': 'Gerald',
    'author_email': 'gera2ld@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/json-server.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
