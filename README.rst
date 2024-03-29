Developing
==========

Please note that it is not required to follow the instructions below in other
to run the ``validator``.  If all you want is to run the Web application,
follow the instructions found in the ``README.rst`` file within the
``validator``.

The following instructions apply to the minimal installation of Ubuntu 9.10.
See <https://help.ubuntu.com/community/Installation/MinimalCD> for details.

To begin with, you need to install the required packages::

  $ sudo apt-get -y install gcc git-core libxslt-dev python-dev python-librdf

Aside of these packages, the following dependencies will also be installed:
binutils gcc-4.4 libc-dev-bin libc6-dev libdigest-sha1-perl liberror-perl
libgomp1 libmysqlclient16 libpq5 libpython2.6 libraptor1 librasqal1 librdf0
libxml2-dev libxslt1-dev libxslt1.1 linux-libc-dev mysql-common patch
python2.6-dev raptor-utils redland-utils zlib1g-dev

These packages require approximately 79.7 MiB (in case of the minimal
installation) and 29.0 MiB (in case of the standard installation).

It is now time to pull the source code from the repositories hosted by
Creative Commons::

  $ mkdir ~/deploy
  $ cd ~/deploy
  $ git clone git@github.com:cc-archive/libvalidator.git

Once you have retrieved both repositories, you can build ``libvalidator``
using the development configuration::

  $ cd ./libvalidator
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
using easy_install, pip, or another method.  If you choose the easy_install
method, you need to install python-setuptools and python-pkg-resources
(1.1 MiB in total) first::

  $ sudo apt-get -y install python-setuptools

Then you need to hatch the egg of ``libvalidator``::

  $ ./bin/python setup.py bdist_egg

What follows depends on whether you would like to have a system-wide
installation or not.  In case of a system-wide installation, all you need
to do is to issue the following command::

  $ sudo easy_install -f ./eggs/ dist/*

However, when it comes to the local availability of the egg, you need
to set up the environment first::

  $ mkdir -p ~/.python/bin  ~/.python/cache ~/.python/lib/site-packages
  $ export PATH="$PATH:$HOME/.python/bin"
  $ export PYTHON_EGG_CACHE="$HOME/.python/cache"
  $ export PYTHONPATH="$PYTHONPATH:$HOME/.python/lib/site-packages/"

Afterwards, install the library in the following manner::

  $ easy_install --install-dir ~/.python/lib/site-packages \
                 --prefix ~/.python -f ./eggs/ dist/*
