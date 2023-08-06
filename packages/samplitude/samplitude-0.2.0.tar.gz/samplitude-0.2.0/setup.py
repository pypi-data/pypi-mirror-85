#!/usr/bin/env python3

from setuptools import setup

import os

__pgdr = 'PG Drange <pgdr@equinor.com>'
__source = 'https://github.com/pgdr/samplitude'
__webpage = __source
__description = "Samplitude (s8e) is a statistical distributions command line tool"

requirements = {
  'minimum': ['numpy>=1.11', 'Jinja2'],
  'csv': ['numpy>=1.11', 'Jinja2', 'pandas'],
  'sci': ['numpy>=1.11', 'Jinja2', 'scipy'],
  'csv_sci': ['numpy>=1.11', 'Jinja2', 'pandas', 'scipy'],
  'plot': ['numpy>=1.11', 'Jinja2', 'matplotlib']
}
requirements['complete'] = sorted(set(sum(requirements.values(), [])))


def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))


def _read_file(fname, op):
    with open(src(fname), 'r') as fin:
        return op(fin.readlines())


def readme():
    try:
        return _read_file('README.md',
                          lambda lines: ''.join(lines))
    except:
        return __description

setup(
    name='samplitude',
    packages=['samplitude'],
    description=__description,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='PG Drange',
    author_email='pgdr@equinor.com',
    maintainer=__pgdr,
    url=__webpage,
    project_urls={
        'Bug Tracker': '{}/issues'.format(__source),
        'Documentation': '{}/blob/master/README.md'.format(__source),
        'Source Code': __source,
    },
    license='GNU GPL v3 or later',
    keywords='jinja2 jinja random statistics sample distribution plot',
    version='0.2.0',
    install_requires=requirements['minimum'],
    entry_points={
        'console_scripts': [
            'samplitude = samplitude:main',
            's8e = samplitude:main',
        ],
    },
    test_suite='tests',
    extras_require=requirements
)
