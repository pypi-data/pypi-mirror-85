========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/symmetrical_chainsaw/badge/?style=flat
    :target: https://readthedocs.org/projects/symmetrical_chainsaw
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/yangchoo/symmetrical_chainsaw.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/yangchoo/symmetrical_chainsaw

.. |version| image:: https://img.shields.io/pypi/v/symmetrical_chainsaw.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/symmetrical_chainsaw

.. |wheel| image:: https://img.shields.io/pypi/wheel/symmetrical_chainsaw.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/symmetrical_chainsaw

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/symmetrical_chainsaw.svg
    :alt: Supported versions
    :target: https://pypi.org/project/symmetrical_chainsaw

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/symmetrical_chainsaw.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/symmetrical_chainsaw

.. |commits-since| image:: https://img.shields.io/github/commits-since/yangchoo/symmetrical_chainsaw/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/yangchoo/symmetrical_chainsaw/compare/v0.0.0...master



.. end-badges

Travis playground. Test.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install symmetrical_chainsaw

You can also install the in-development version with::

    pip install https://github.com/yangchoo/symmetrical_chainsaw/archive/master.zip


Documentation
=============


https://symmetrical_chainsaw.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
