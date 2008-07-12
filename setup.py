from setuptools import setup, find_packages

setup(
    name='libvalidator',
    version='0.1',
    description='A library that parses (X)HTML for RDF with regard to licensing.',
    author='Hugo Dworak',
    #author_email='',
    #url='',
    install_requires=['setuptools',
                      'nose',
                      'html5lib',
                      'rdflib',
                      'BeautifulSoup',
                      'pyRdfa'
                      ],
    packages=find_packages(exclude=['ez_setup',]),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'libvalidator': ['tests/*']},
)

