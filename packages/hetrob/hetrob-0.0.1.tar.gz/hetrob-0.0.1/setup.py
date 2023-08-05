#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('VERSION') as version_file:
    version = version_file.read()

requirements = [
    'Click>=7.0',
    'numpy>=1.19.0',
    'matplotlib>=3.1.2',
    'deap>=1.3.1',
    'psutil>=5.7.2'
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jonas Teufel",
    author_email='jonseb1998@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python package for the optimzation of schedules for heterogeneous, cooperating robot teams",
    entry_points={
        'console_scripts': [
            'hetrob=hetrob.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    package_data={
        '': ['*.json']
    },
    include_package_data=True,
    keywords='hetrob',
    name='hetrob',
    packages=find_packages(include=['hetrob', 'hetrob.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/the16thpythonist/hetrob',
    version=version,
    zip_safe=False,
)
