#!/usr/bin/env python2

from setuptools import setup
import os
import re
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    """
    Get the long description from a file.
    """
    fname = os.path.join(here, filename)
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


test_deps = ['nose2']

setup(
    name='sllurp',
    version='0.1.8.1',
    description=read('README.md'),
    author='Ben Ransford',
    author_email='ben@ransford.org',
    url='https://github.com/ransford/sllurp',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    keywords='llrp rfid reader',
    packages=['sllurp'],
    install_requires=['click', 'twisted'],
    tests_require=test_deps,
    extras_require={'test': test_deps},
    entry_points={
        'console_scripts': [
            'sllurp=sllurp.cli:cli',
        ],
    },
)
