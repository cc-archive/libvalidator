Developing
==========

The following instructions apply to the minimal installation of Ubuntu 9.10.
See <https://help.ubuntu.com/community/Installation/MinimalCD> for details.

To begin with, you need to install the required packages::

  $ sudo apt-get -y install gcc git-core libxslt-dev python-dev python-librdf

Aside of these packages, the following dependencies will also be installed:
binutils gcc-4.4 libc-dev-bin libc6-dev libdigest-sha1-perl liberror-perl
libgomp1 libmysqlclient16 libpq5 libpython2.6 libraptor1 librasqal1 librdf0
libxml2-dev libxslt1-dev libxslt1.1 linux-libc-dev mysql-common patch
python2.6-dev raptor-utils redland-utils zlib1g-dev

These packages require approximately 79.7 MB (in case of the minimal
installation) and 29.0 MB (in case of the standard installation).

It is now time to pull the source code from the repositories hosted by
Creative Commons::

  $ mkdir ~/deploy
  $ cd ~/deploy
  $ git clone git://code.creativecommons.org/libvalidator.git
  $ cd ./libvalidator

Once you have retrieved both repositories, you can build ``validator``
using the development configuration::

  $ python ./bootstrap.py
  $ ./bin/buildout

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
Python and ``libvalidator`` you are using.

