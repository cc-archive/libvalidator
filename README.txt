Installation and Setup
======================

The following instructions apply to Ubuntu 8.10 Intrepid Ibex.

$ sudo aptitude install libxml2-dev libxslt1-dev python-librdf python-setuptools

$ mkdir -p ~/.python/lib/python2.5/site-packages ~/deploy
$ export PYTHONPATH="$PYTHONPATH:$HOME/.python/lib/python2.5/site-packages/"
$ export PATH="$PATH:$HOME/.python/bin"
$ export PYTHON_EGG_CACHE="$HOME/.python/cache"
$ cd ~/deploy
$ easy_install --install-dir ~/.python/lib/python2.5/site-packages \
  --prefix ~/.python virtualenv zc.buildout

$ git clone git://code.creativecommons.org/cc.license.git
$ cd cc.license
$ git submodule init
$ git submodule update
$ virtualenv --no-site-packages .
$ python bootstrap/bootstrap.py
$ buildout
$ buildout install
$ python setup.py bdist_egg
$ easy_install --install-dir ~/.python/lib/python2.5/site-packages \
  --prefix ~/.python dist/*
$ cd ..

$ git clone git://code.creativecommons.org/libvalidator.git
$ cd libvalidator
$ git submodule init
$ git submodule update
$ virtualenv --no-site-packages .
$ python bootstrap/bootstrap.py
$ buildout
$ buildout install
$ python setup.py bdist_egg
$ easy_install --install-dir ~/.python/lib/python2.5/site-packages \
  --prefix ~/.python dist/*

$ nosetests
