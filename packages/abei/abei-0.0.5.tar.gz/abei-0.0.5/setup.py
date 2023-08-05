#!/usr/bin/env python

import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('abei/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='abei',
    version=version,
    description='Library for Functional Graphic Programming',
    long_description=readme,
    packages=[
        'abei',
        'abei.interfaces',
        'abei.interfaces.procedure',
        'abei.implements',
    ],
    install_requires=[],
    include_package_data=True,
    url='https://www.mind-bricks.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
