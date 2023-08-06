#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup  # type: ignore

with open('README.rst') as readme_file:
    long_description = readme_file.read()

requirements = [
    'beautifulsoup4',
    'lxml',
    'requests',
]

test_requirements = [
    'pytest>=3',
]

setup(
    author='Oliver Stapel',
    author_email='hardy.ecc95@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: Other/Nonlisted Topic',
    ],
    description='Collections of academic degrees for the US, the UK, and Germany.',  # noqa
    install_requires=requirements,
    license='MIT license',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='person, titles, degrees',
    name='persontitles',
    packages=find_packages(exclude=('tests',)),  # noqa
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/0LL13/persontitles',
    version='0.1.3',
    zip_safe=False,
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest-cov'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/0LL13/persontitles/issues',
        'Source': 'https://github.com/0LL13/persontitles',
    },
)
