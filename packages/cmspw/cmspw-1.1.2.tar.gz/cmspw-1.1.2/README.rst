
CMS password generator
======================


.. image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
   :alt: LICENSE


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: STYLE


.. image:: https://img.shields.io/circleci/build/gh/trussworks/cmspw
   :target: https://circleci.com/gh/trussworks/cmspw/tree/master
   :alt: CIRCLECI


EUA
---

EUA rules implemented in this script are:


* Must start with a letter
* At least one number (0-9)
* At least one Lowercase alphabetic character (a-z)
* At least one Upper Case alphabetic character (A-Z)
* MUST BE EXACTLY 8 characters long
* May not include "punctuation characters" (undocumented)

Rules NOT implemented:


* Cannot include your EUA UserID and any part of your name
* Cannot include any word/word portion prohibited by the defined CMS dictionary
* Password can’t contain 50% characters from previous password
* Be different from the previous 24 passwords

CloudVPN
--------

CloudVPN rules implemented in this script are:


* Cannot contain keyboard walks of 3 or more consecutive keyboard keys in a row
  (e.g. asd, zaq, 123, was, pol, ser, gyu, bhj, 9o0, p;[, etc.)
* Password length greater than 15 characters.
* Contain 3 out of 4 the following:

  * 1 digits (0-9).
  * 1 symbols (!, @, #, $, %, \*, etc.).
  * 1 uppercase English letters (A-Z).
  * 1 lowercase English letters (a-z).

Rules NOT implemented:


* Password must differ from previous password by 24 password(s).
* Password must be at least 1day(s) since last password change.

Installation
------------

You need python3:

.. code-block:: console

   brew install python3
   python3 -m pip install cmspw

Usage
-----

Cryptographically random alphanumeric strings are generated, printing the first
that complies with the EUA/CloudVPN ruleset to the standard output.

.. code-block:: console

   $ python3 -m cmspw --help
   usage: cmspw [-h] --ruleset RULESET [--length NUM]

   generates passwords for CMS

   optional arguments:
     -h, --help            show this help message and exit
     --ruleset RULESET, -r RULESET
                           rule set to validate against. can be one of ['eua', 'vpn'].
     --length NUM, -l NUM  password length. if ruleset is 'eua', this is ignored.
   $ python3 -m cmspw --ruleset eua
   qJbcNJ2Y
   $ python3 -m cmspw --ruleset vpn --length 24
   4H+-X^#XV(8'&wB5ZNn'H%>q

Development
-----------

You need poetry:

.. code-block:: console

   brew install poetry

Inside the project directory you can enter a virtual environment like so:

.. code-block:: console

   poetry install && poetry shell
