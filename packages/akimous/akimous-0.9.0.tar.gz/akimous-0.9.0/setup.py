# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akimous',
 'akimous.modeling',
 'akimous.modeling.feature',
 'akimous.resources',
 'akimous.resources.doc_template',
 'akimous.resources.file_templates.helloworld',
 'akimous.resources.file_templates.setup',
 'akimous_ui']

package_data = \
{'': ['*'],
 'akimous.resources': ['file_templates/dockerfile/*',
                       'file_templates/gitignore/*',
                       'file_templates/license/*',
                       'file_templates/readme/*',
                       'file_templates/tox/*']}

install_requires = \
['Send2Trash>=1.5,<2.0',
 'appdirs>=1.4,<2.0',
 'cachetools>=4.0,<5.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'gitpython>=3.1.0,<4.0.0',
 'ipykernel>=5.1,<6.0',
 'jedi>=0.17.0,<0.18.0',
 'jupyter_client>=6.0,<7.0',
 'logzero>=1.5,<2.0',
 'msgpack>=1.0,<2.0',
 'numpy>=1.17,<2.0',
 'numpydoc>=1.0.0,<2.0.0',
 'pathspec>=0.8.0,<0.9.0',
 'ptyprocess>=0.6.0,<0.7.0',
 'pyflakes>=2.0,<3.0',
 'pylint>=2.1,<3.0',
 'python-levenshtein>=0.12.0,<0.13.0',
 'sphinx>=3.0,<4.0',
 'toml>=0.10.0,<0.11.0',
 'watchdog>=0.10.0,<0.11.0',
 'websockets>=8.0,<9.0',
 'wordsegment>=1.3,<2.0',
 'xgboost>=1.0,<2.0',
 'yapf>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['akimous = akimous.__main__:start']}

setup_kwargs = {
    'name': 'akimous',
    'version': '0.9.0',
    'description': 'An intelligent Python IDE',
    'long_description': '# Akimous\n\n[![PyPI version](https://badge.fury.io/py/akimous.svg)](https://pypi.python.org/pypi/akimous/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/akimous.svg)](https://pypi.python.org/pypi/akimous/) [![CircleCI](https://circleci.com/gh/akimous/akimous/tree/master.svg?style=svg)](https://circleci.com/gh/akimous/akimous/tree/master)\n\nAkimous is a Python IDE with unique features boosting developers\' productivity.\n\n### Features\n\n* Machine-learning-assisted/NLP-assisted context-aware auto completion\n* Beautifully rendered function documentation\n* Layered keyboard control (a more intuitive key binding than vim and Emacs)\n* Real-time code formatter\n* Interactive console (integration with IPython kernel)\n\n<img src="https://raw.githubusercontent.com/akimous/akimous/master/images/screenshot.png" alt="Screenshot" style="max-width:100%">\n\nFor more information and documentation, visit the official website.\n\n## Installation\n\n### Prerequisite\n\n* Python 3.7 or 3.8 (with pip)\n* Git (for version control integration)\n* C/C++ compiler (may be required by some dependencies during installation)\n* A modern browser\n\n### Installing From PyPI\n\nThe recommended way for installing Akimous is through PyPI.\n\n```sh\npip install -U akimous\n```\n\n### Starting Application\n\nStart it in the terminal. The browser should be automatically opened.\n\n```sh\nakimous\n```\n\n* To see available arguments, do `akimous --help`.\n\n### Using Docker Image\n\nIf you have difficulty installing, or you are running in a cloud environment, try the prebuilt docker image.\n\n```sh\ndocker run --mount type=bind,source=$HOME,target=/home/user -p 127.0.0.1:3179:3179 -it red8012/akimous akimous\n```\n\n## Commands\n\nStart the app by typing in the terminal (the browser will automatically open if available): \n\n```sh\nakimous\n```\n\n#### Options\n\n* `--help`: show help message and exit.\n* `--host HOST`: specify the host for Akimous server to listen on. (default to 0.0.0.0 if inside docker, otherwise 127.0.0.1)\n* `--port PORT`: The port number for Akimous server to listen on. (default=3179)\n* `--no-browser`: Do not open the IDE in a browser after startup.\n* `--verbose`: Print extra debug messages.\n\n## Development\n\nMake sure you have recent version of the following build dependencies installed.\n\n* Node (12+)\n* Python (3.7+)\n* [Poetry](https://poetry.eustace.io)\n* [Yarn](https://yarnpkg.com/)\n* Make\n* [Zopfli](https://github.com/google/zopfli)\n* [Parallel](https://www.gnu.org/software/parallel/)\n\nRun the following commands according to your need.\n\n```sh\nmake # build everything\nmake test # run tests\nmake lint # run linters\nmake install # (re)install the package\n```\n\nRunning `make` will install all Python and Javascript dependencies listed in `pyproject.toml` and `ui/package.json` automatically.\n\n## Contributing\n\nThis program is at pre-alpha stage. Please do report issues if you run into some problems. Contributions of any kind are welcome, including feature requests or pull requests (can be as small as correcting spelling errors) . \n\n## License\n\n[BSD-3-Clause](LICENSE)\n\n## Links\n\n* [Official website](https://akimous.com)\n* [PyPI](https://pypi.org/project/akimous/)\n* [Docker Hub](https://hub.docker.com/r/red8012/akimous)\n\n',
    'author': 'Yu-Ann Chen',
    'author_email': 'red8012@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://akimous.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
