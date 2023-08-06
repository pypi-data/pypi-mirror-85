==========
Change Log
==========

All notable changes to this project will be documented here.

Sort subsections like so: Added, Bugfixes, Improvements, Technical tasks.
Group anything an end user shouldn't care deeply about into technical
tasks, even if they're technically bugs. Only include as "bugfixes"
bugs with user-visible outcomes.

When major components get significant changes worthy of mention, they
can be described in a Major section.

v2.1.0 - Unreleased
===================

Added
-----

* Official docker image

Bugfixes
--------

* Document what migratron does
* Exception message is valid when using Python2 and Python3
* Make the subcommand required and print the help message if missing

Technical Tasks
---------------

* Improve the documentation on how to setup migratron locally
* Add documentation on how to run the tests
* Add documentation on how migratron works


v2.0.1 - 2020-09-29
===================

Bugfixes
--------

* Added VERSION file to the python package

v2.0.0 - 2020-08-28
===================

Added
-----

* Options to run the migration against Hive or Presto
* Created the documentation
* The project can be used on Python3
* Description to the README.rst

Changed
-------

* Rename the package to migratron
* Changed the ``--database-uri|type`` parameters to ``--db-uri|type``

Bugfixes
--------

* Added requirements-dev.txt to setup.py package_data
* Missing requirements.txt when using pip to install package
* Use Python 2 and 3 compatible function to get user input

Technical Task
--------------

* Do not use unittest deprecated methods
* Generate coverage report when running the tests
* Added missing classifiers to setup.py
* Create a version file
* Format the code using black
* Add Makefile to run tests and generate documentation
* Solve typos and improve documentation
* Fix min required version for some dev dependencies
* Added readthedocs configuration file
* Added long description to the setup.py
* Use MANIFEST.ini to add non python files to the package<Paste>
