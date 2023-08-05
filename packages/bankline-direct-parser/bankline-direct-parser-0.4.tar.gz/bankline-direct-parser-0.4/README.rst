Bankline Direct Parser
======================

Python module for parsing Natwest/RBS Bankline Direct Data Services files.


Requirements
------------

Only python 3.4+ supported.


Installation
------------

.. code-block:: bash

    pip install bankline-direct-parser


Usage
-----

.. code-block:: python

    from bankline_parser.data_services import parse

    # from file
    with open(filename) as f:
        parsed = parse(f)
        if parsed.is_valid():
            print(parsed.accounts[0].records[0].transaction_code)
        else:
            print(parsed.errors)

    # from list of rows
    parsed = parse(lines)


Model Layout
------------

.. code-block::

    DataServicesFile
        VolumeHeaderLabel
        [Account]
            FileHeaderLabel
            UserHeaderLabel
            [DataRecord|BalanceRecord]
            UserTrailerLabel


Development
-----------

.. image:: https://github.com/ministryofjustice/bankline-direct-parser/workflows/Run%20tests/badge.svg?branch=master
    :target: https://github.com/ministryofjustice/bankline-direct-parser/actions


Please report bugs and open pull requests on `GitHub`_.

Use ``python setup.py test`` or ``tox`` to run all tests.

Distribute a new version by updating the ``VERSION`` tuple in ``bankline_parser/__init__.py`` and
publishing a release in GitHub (this triggers a GitHub Actions workflow to automatically upload it).
Alternatively, run ``python setup.py sdist bdist_wheel upload`` locally.


Copyright
---------

Copyright (C) 2020 HM Government (Ministry of Justice Digital & Technology).
See LICENSE.txt for further details.

.. _GitHub: https://github.com/ministryofjustice/bankline-direct-parser
