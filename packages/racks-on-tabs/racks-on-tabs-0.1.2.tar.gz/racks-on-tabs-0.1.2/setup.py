# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['racks_on_tabs']

package_data = \
{'': ['*'],
 'racks_on_tabs': ['static/app.css',
                   'static/app.css',
                   'static/app.css',
                   'static/app.js',
                   'static/app.js',
                   'static/app.js',
                   'static/favicon.png',
                   'static/favicon.png',
                   'static/favicon.png',
                   'templates/*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'waitress>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['racks-on-tabs = racks_on_tabs.__main__:main']}

setup_kwargs = {
    'name': 'racks-on-tabs',
    'version': '0.1.2',
    'description': 'Command line app for browsing CSV files with row lazy loading.',
    'long_description': '# racks-on-tabs\n\n> (What you got?) Racks on tabs on tabs\n>\n> (He got) Racks on tabs on tabs\n>\n> (We got) Racks on tabs on taaabs\n>\n> ~[YC & Future, circa 2011, probably](https://www.youtube.com/watch?v=r5w21_Vphbg&ab_channel=ycvevo)\n\nCommand line app for browsing CSV files with row lazy loading.\n\n![](docs/imgs/1m-csv-example.png)\n*This is what opening [1M rows](http://eforexcel.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/) under 100ms looks like.*\n\n```sh\n$ racks-on-tabs <PATH_TO_CSV>\n```\n\nStarts a local webserver that serves the app content, accessible at [localhost:7482](http://localhost:7482).\n\n# Installation\n\nRequires Python 3. Tested with Python 3.8.\n\n## pipx\n\n_racks-on-tabs_ is a Python app with a set of dependencies.\nThe recommended way to install it is via [pipx](https://github.com/pipxproject/pipx):\n\n```sh\n$ pipx install racks-on-tabs\n$ racks-on-tabs <PATH_TO_CSV>\n```\n\n## virtualenv\n\nAlternatively, you can set up a local virtual env and install _racks-on-tabs_ there:\n\n```sh\n$ python3 -m venv venv\n$ source venv/bin/activate\n$ pip3 install racks-on-tabs\n$ racks-on-tabs <PATH_TO_CSV>\n```\n\n## Troubleshooting\n\nIf for some reason you get "executable not found" errors, try locating the library installation path, and run:\n\n```sh\n$ python -m path/to/pip/packages/racks_on_tabs.__main__ <PATH_TO_CSV>\n```\n\n',
    'author': 'Alexander Juda',
    'author_email': 'alexanderjuda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexjuda/racks-on-tabs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
