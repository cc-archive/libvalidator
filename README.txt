Installation and Setup
======================

The following instructions apply to Ubuntu 8.04 Hardy Heron.

$ sudo apt-get install python-librdf python-setuptools python-lxml python-zopeinterface
$ sudo easy_install zc.buildout virtualenv
$ mkdir ~/deploy
$ cd ~/deploy
$ git clone git://code.creativecommons.org/libvalidator.git
$ cd libvalidator
$ git submodule init
$ git submodule update
$ virtualenv --no-site-packages .
$ python bootstrap/bootstrap.py
$ buildout
$ buildout install
$ python setup.py bdist_egg
$ sudo easy_install eggs/pyRdfa-2.0-py2.5.egg dist/libvalidator-0.0.0-py2.5.egg
$ nosetests
