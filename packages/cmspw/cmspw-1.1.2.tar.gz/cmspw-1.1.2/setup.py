# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmspw', 'cmspw.data']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cmspw = cmspw.__main__:main']}

setup_kwargs = {
    'name': 'cmspw',
    'version': '1.1.2',
    'description': 'generates passwords for CMS',
    'long_description': '\nCMS password generator\n======================\n\n\n.. image:: https://img.shields.io/badge/license-Apache%202.0-informational\n   :target: https://www.apache.org/licenses/LICENSE-2.0.txt\n   :alt: LICENSE\n\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: STYLE\n\n\n.. image:: https://img.shields.io/circleci/build/gh/trussworks/cmspw\n   :target: https://circleci.com/gh/trussworks/cmspw/tree/master\n   :alt: CIRCLECI\n\n\nEUA\n---\n\nEUA rules implemented in this script are:\n\n\n* Must start with a letter\n* At least one number (0-9)\n* At least one Lowercase alphabetic character (a-z)\n* At least one Upper Case alphabetic character (A-Z)\n* MUST BE EXACTLY 8 characters long\n* May not include "punctuation characters" (undocumented)\n\nRules NOT implemented:\n\n\n* Cannot include your EUA UserID and any part of your name\n* Cannot include any word/word portion prohibited by the defined CMS dictionary\n* Password can’t contain 50% characters from previous password\n* Be different from the previous 24 passwords\n\nCloudVPN\n--------\n\nCloudVPN rules implemented in this script are:\n\n\n* Cannot contain keyboard walks of 3 or more consecutive keyboard keys in a row\n  (e.g. asd, zaq, 123, was, pol, ser, gyu, bhj, 9o0, p;[, etc.)\n* Password length greater than 15 characters.\n* Contain 3 out of 4 the following:\n\n  * 1 digits (0-9).\n  * 1 symbols (!, @, #, $, %, \\*, etc.).\n  * 1 uppercase English letters (A-Z).\n  * 1 lowercase English letters (a-z).\n\nRules NOT implemented:\n\n\n* Password must differ from previous password by 24 password(s).\n* Password must be at least 1day(s) since last password change.\n\nInstallation\n------------\n\nYou need python3:\n\n.. code-block:: console\n\n   brew install python3\n   python3 -m pip install cmspw\n\nUsage\n-----\n\nCryptographically random alphanumeric strings are generated, printing the first\nthat complies with the EUA/CloudVPN ruleset to the standard output.\n\n.. code-block:: console\n\n   $ python3 -m cmspw --help\n   usage: cmspw [-h] --ruleset RULESET [--length NUM]\n\n   generates passwords for CMS\n\n   optional arguments:\n     -h, --help            show this help message and exit\n     --ruleset RULESET, -r RULESET\n                           rule set to validate against. can be one of [\'eua\', \'vpn\'].\n     --length NUM, -l NUM  password length. if ruleset is \'eua\', this is ignored.\n   $ python3 -m cmspw --ruleset eua\n   qJbcNJ2Y\n   $ python3 -m cmspw --ruleset vpn --length 24\n   4H+-X^#XV(8\'&wB5ZNn\'H%>q\n\nDevelopment\n-----------\n\nYou need poetry:\n\n.. code-block:: console\n\n   brew install poetry\n\nInside the project directory you can enter a virtual environment like so:\n\n.. code-block:: console\n\n   poetry install && poetry shell\n',
    'author': 'Ryan Delaney',
    'author_email': 'ryan@truss.works',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/cmspw/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
