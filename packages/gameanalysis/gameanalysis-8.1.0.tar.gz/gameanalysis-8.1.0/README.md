Game Analysis
=============

[![build](https://github.com/egtaonline/gameanalysis/workflows/build/badge.svg)](https://github.com/egtaonline/gameanalysis/actions)

This is a collection of python libraries and scripts that manipulate empirical game data.


Usage Setup
-----------

This package is hosted on pypi. Install it with `pip install gameanalysis`.

The entry point from the command line is `ga`. `ga --help` will document all
available options.

The entry point for python is `gameanalysis`. See the documentation for what is
available from the python interface.


Developing
==========

After cloning this repository, the included `Makefile` includes all the relevant actions to facilitate development.
Typing `make` without targets will print out the various actions to help development.
Type `make setup` to configure a virtual environment for development.


Requirements
------------

1. Python 3 & venv
2. BLAS/LAPACK
3. A fortran compiler


Testing
-------

All of the tests can be run with `make test`.
Running `make check` will search for style compliance, and `make format` will try to fix some in places.
`make docs` will make the documentation.
