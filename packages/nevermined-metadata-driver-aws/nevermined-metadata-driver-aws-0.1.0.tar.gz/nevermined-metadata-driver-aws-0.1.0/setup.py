#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

# Installed by pip install metadata-driver-aws
# or pip install -e .
install_requirements = [
    'coloredlogs',
    'boto3 == 1.8.7',
    'PyYAML>=4.2b1',
    'nevermined-metadata-driver-interface==0.1.0',
]

# Required to run setup.py:
setup_requirements = ['pytest-runner', ]

test_requirements = [
    'codacy-coverage',
    'coverage',
    'pylint',
    'pytest',
    'pytest-watch',
    'tox',
]

# Possibly required by developers of metadata-driver-aws:
dev_requirements = [
    'bumpversion',
    'pkginfo',
    'twine',
    'watchdog',
]

setup(
    author="nevermined-io",
    author_email='root@nevermined.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="💧 Metadata S3 Driver Implementation",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='nevermined-metadata-driver-aws',
    name='nevermined-metadata-driver-aws',
    packages=find_packages(include=['metadata_driver_aws']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nevermined-io/metadata-driver-aws',
    version='0.1.0',
    zip_safe=False,
)
