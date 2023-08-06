# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibliophile',
 'bibliophile.bibliocommons',
 'bibliophile.goodreads',
 'bibliophile.tests',
 'bibliophile.tests.bibliocommons',
 'bibliophile.tests.goodreads']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4', 'grequests', 'lxml', 'requests']

setup_kwargs = {
    'name': 'bibliophile',
    'version': '0.1.2',
    'description': 'Find books at your local library',
    'long_description': '[![Build Status](https://travis-ci.com/DavidCain/bibliophile-backend.svg?branch=master)](https://travis-ci.com/DavidCain/bibliophile-backend)\n[![Code Coverage](https://codecov.io/gh/DavidCain/bibliophile-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/DavidCain/bibliophile-backend)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n# Bibliophile backend\nThis is a Python-based tool for finding books at the local library.\n\nIt parses your "to read" list from Goodreads.com and checks which items\nare available at a library of your choosing.\n\n## Looking for a GUI?\nThis repository is all you need to use the tool locally via the command line.\nFor a web-based user interface, see [Bibliophile][bibliophile-repo].\n\n# Can I use this?\nIf you live near one of the ~190 public libraries using the BiblioCommons\nsystem, then running this software should work for you. It relies on\nundocumented APIs, so your mileage may vary.\n\n1. Apply for a [Goodreads Developer Key][goodreads-api].\n2. Obtain your Goodreads user id\n3. [Optional] Set both these values in your `.bashrc`\n\n    ```sh\n    export GOODREADS_USER_ID=123456789\n    export GOODREADS_DEV_KEY=whatever-your-actual-key-is\n    ```\n4. [Install Poetry][poetry-install]\n5. Run the script!\n\n    ```sh\n    make  # One-time setup of dependencies\n    ./lookup.py --biblio seattle  # Set to your own city!\n    ```\n\nMake sure you adhere to the terms of [Goodreads\' API][goodreads-api-terms], and\nhave fun.\n\n## Other options\nYou can choose to show only titles available at your local branch, select titles\nfrom another Goodreads shelf, etc. Pass `--help` to see all options:\n\n```\nusage: lookup.py [-h] [--branch BRANCH] [--shelf SHELF] [--biblio BIBLIO]\n                 [--csv CSV]\n                 [user_id] [dev_key]\n\nSee which books you want to read are available at your local library.\n\npositional arguments:\n  user_id          User\'s ID on Goodreads\n  dev_key          Goodreads developer key. See https://www.goodreads.com/api\n\noptional arguments:\n  -h, --help       show this help message and exit\n  --branch BRANCH  Only show titles available at this branch. e.g. \'Fremont\n                   Branch\'\n  --shelf SHELF    Name of the shelf containing desired books\n  --biblio BIBLIO  subdomain of bibliocommons.com (seattle, vpl, etc.)\n  --csv CSV        Output results to a CSV of this name.\n```\n\n## Cloud-based deployment\nThis may also be deployed as Lambda functions in AWS.\nSee the [Bibliophile README][bibliophile-repo] for instructions.\n\n\n[bibliophile-repo]: https://github.com/DavidCain/bibliophile\n[goodreads-api]: https://www.goodreads.com/api\n[goodreads-api-terms]: https://www.goodreads.com/api/terms\n[poetry-install]: https://python-poetry.org/docs/#installation\n',
    'author': 'David Cain',
    'author_email': 'davidjosephcain@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://biblo.dcain.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
