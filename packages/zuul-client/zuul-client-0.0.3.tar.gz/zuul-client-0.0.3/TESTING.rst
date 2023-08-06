=================
Testing Your Code
=================
------------
A Quickstart
------------

This is designed to be enough information for you to run your first tests.

*Install pip*::

  [apt-get | yum] install python-pip

More information on pip here: http://www.pip-installer.org/en/latest/

*Use pip to install tox*::

  pip install tox

Run The Tests
-------------

*Navigate to the project's root directory and execute*::

  tox

Information about tox can be found here: http://testrun.org/tox/latest/


Run The Tests in One Environment
--------------------------------

Tox will run your entire test suite in the environments specified in the project tox.ini::

  [tox]

  envlist = <list of available environments>

To run the test suite in just one of the environments in envlist execute::

  tox -e <env>
so for example, *run the test suite in py36*::

  tox -e py36

Run One Test
------------

To run individual tests with tox::

  tox -e <env> -- path.to.module.Class.test
