from setuptools import setup, find_packages

setup(
    name='libvalidator',
    version='0.1',
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=['setuptools',
                      'nose',
                      ],
    packages=find_packages(exclude=['ez_setup',]),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'libvalidator': ['tests/*']},
)

