from setuptools import setup, find_packages

setup(
    name='libvalidator',
    author='Hugo Dworak',
    install_requires=['setuptools',
                      'nose',
                      'html5lib',
                      'rdflib == 2.4.0',
                      'pyRdfa',
                      'chardet',
                      'BeautifulSoup',
                      'lxml',
                      'cc.license'
                      ],
    packages=find_packages(exclude=['ez_setup',]),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'libvalidator': ['tests/*']},
)

