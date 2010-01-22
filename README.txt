
Developing
==========

``libvalidator`` uses `buildout`_ for managing the build and
deployment process.  After checking out the ``libvalidator``
repository, do the following to begin developing it::

  $ cd libvalidator
  $ python bootstrap.py
  $ ./bin/buildout

Buildout will install the dependencies needed to work with
libvalidator.  You may need additional libraries installed in order to
build some of the dependencies.  On Ubuntu these include libxml2-dev,
libxslt1-dev, python-librdf, and python-dev.

Testing
=======

Buildout will create a test runner in the ``bin`` directory.  You can
run the full test suite by running::

  $ ./bin/nosetests

Installing
==========

To install ``libvalidator``, first build the egg, and then install it
using easy_install, pip, or another method::

  $ ./bin/python setup.py bdist_egg
  $ easy_install ./dist/libvalidator-0.0.0-py2.6.egg

The specific egg filename may differ based on the version of
libvalidator and Python you are using.

