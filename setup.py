# -*- coding: utf-8 -*-
""" The setup script.

Copyright (C) 2008, 2009, 2010 Robert Gust‐Bardon and Creative Commons.
Originally contributed by Asheesh Laroia.

This file is part of the License Validation Library.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from setuptools import setup, find_packages

__author__ = "Robert Gust‐Bardon and Creative Commons"
__copyright__ = ("Copyright 2008, 2009, 2010 "
                 "Robert Gust‐Bardon and Creative Commons")
__credits__ = ["Asheesh Laroia", "Robert Gust‐Bardon"]
__license__ = ("GNU Lesser General Public License Version 3 "
               "or any later version")
__version__ = "0.1.0"
__maintainer__ = "Robert Gust‐Bardon"
__status__ = "Beta"

README = os.path.join(os.path.dirname(__file__), "README.txt")
long_description = open(README).read()

setup(
    name="libvalidator",
    version=__version__,
    description=("The library that is used by the License Validation Service "
                 "to obtain the information about licensed objects"),
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        ("License :: OSI Approved :: "
         "GNU Library or Lesser General Public License (LGPL)"),
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities"
        ],
    keywords="license licence extraction validation verification checking",
    author="Robert Gust‐Bardon and Creative Commons",
    url="http://validator.creativecommons.org/",
    license=("GNU Lesser General Public License Version 3 "
             "or any later version"),
    packages=find_packages(exclude=["ez_setup",]),
    install_requires=["setuptools",
                      "nose",
                      "html5lib",
                      "rdflib == 2.4.0",
                      "pyRdfa",
                      "cc.license"
                      ],
    include_package_data=True,
    test_suite="nose.collector",
    package_data={"libvalidator": ["tests/*"]},
    )

