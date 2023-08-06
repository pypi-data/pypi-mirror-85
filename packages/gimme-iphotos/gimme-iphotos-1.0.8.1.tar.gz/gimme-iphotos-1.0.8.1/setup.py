# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gimme_iphotos']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'pyicloud-z>=0.9.7-beta.2,<0.10.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['gimme-iphotos = gimme_iphotos:main']}

setup_kwargs = {
    'name': 'gimme-iphotos',
    'version': '1.0.8.1',
    'description': 'Download photos and videos from iCloud',
    'long_description': "# Gimme-iPhotos\n\n[![PyPI](https://img.shields.io/pypi/v/gimme-iphotos.svg)](https://pypi.python.org/pypi/gimme-iphotos)\n[![PyPI](https://img.shields.io/pypi/l/gimme-iphotos.svg)](https://opensource.org/licenses/MIT)\n\nDownload media files from iCloud.\n\nThis tool uses [pyicloud] to synchronize photos and videos from iCloud to your\nlocal machine.\n\n## Features\n\n- Downloads media files from iCloud in parallel (might be beneficial on small files and wide bandwidth)\n- Keeps local collection in sync with iCloud by:\n  - skipping files which exist locally\n  - removing local files which were removed from the cloud\n- Reads configuration from ini-file\n- Stores password in keychain (provided by [pyicloud])\n- Supports two-factor authentication\n- Shows nice progress bars (thanks to [tqdm])\n\n## Installation\n\n```sh\n$ pip3 install gimme-iphotos\n```\n\nor\n\n```sh\n$ docker pull zebradil/gimme-iphotos\n```\n\n## Usage\n\n```\n$ gimme-iphotos --help\nusage: gimme-iphotos [-h] [-c CONFIG] [-v] [-u USERNAME] [-p PASSWORD] [-d DESTINATION] [-o] [-r] [-n PARALLEL]\n\nDownloads media files from iCloud\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        Configuration file. It's ini-like file (see configparser module docs), must contain [main] section. Keys are fully-named arguments, except help, config and verbose.\n                        Values specified using command line arguments take precedence over values from a provided config file.\n  -v, --verbose\n  -u USERNAME, --username USERNAME\n                        iCloud username (email). Can be specified interactively if not set.\n  -p PASSWORD, --password PASSWORD\n                        iCloud password. Can be specified interactively if not set.\n  -d DESTINATION, --destination DESTINATION\n                        Destination directory. Can be specified interactively if not set.\n  -o, --overwrite       Overwrite existing files. Default: false.\n  -r, --remove          Remove missing files. Default: false.\n  -n PARALLEL, --num-parallel-downloads PARALLEL\n                        Max number of concurrent downloads. Increase this number if bandwidth is not fully utilized. Default: 3\n```\n\nUsing config file:\n\n```sh\n$ cat john.cfg\n[main]\nusername = john.doe@example.com\npassword = not-secure123\ndestination = /home/john/Photos\nremove = True\n\n$ gimme-iphotos -c john.cfg\n```\n\nOverriding config file:\n\n```sh\n$ gimme-iphotos -c john.cfg --destination /tmp/icloud\n```\n\nWithout config file:\n\n```sh\n$ # Password will be requested interactively\n$ gimme-iphotos -u john.doe@rexample.com --destination /tmp/icloud\nEnter iCloud password for john.doe@rexample.com:\n```\n\n### Docker\n\nThe CLI is the same but requires mounting destination directory and config file (if needed).\n\n```sh\n$ docker run -it \\\n    -v <destination>:/somedir \\\n    -v ${PWD}/john.cfg:/app/john.cfg \\\n    zebradil/gimme-iphotos -c john.cfg\n```\n\n## License\n\nLicensed under the [MIT License].\n\nBy [German Lashevich].\n\n[MIT License]: https://github.com/zebradil/Gimme-iPhotos/blob/master/LICENSE\n[pyicloud]: https://github.com/picklepete/pyicloud\n[tqdm]: https://github.com/tqdm/tqdm\n[German Lashevich]: https://github.com/zebradil\n",
    'author': 'German Lashevich',
    'author_email': 'german.lashevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zebradil/Gimme-iPhotos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
