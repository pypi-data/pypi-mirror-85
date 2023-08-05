# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# root path
ROOT = os.path.dirname(os.path.realpath(__file__))

# README
with open(os.path.join(ROOT, 'README.md'), encoding='utf-8') as file:
    long_desc = file.read()

# version string
__version__ = '0.1.5rc1'

# set-up script for pip distribution
setup(
    name='python-walrus',
    version=__version__,
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/pybpc/walrus',
    license='Apache Software License',
    keywords=['walrus operator', 'assignment expression', 'back-port compiler'],
    description='Back-port compiler for Python 3.8 assignment expressions.',
    long_description=long_desc,
    long_description_content_type='text/markdown; charset=UTF-8',
    python_requires='>=3.4',
    zip_safe=True,
    install_requires=[
        'parso>=0.6.0',         # universal AST support
        'tbtrim>=0.2.1',        # traceback trim support
        'f2format>=0.8.6',      # f-string compatibility
        'bpc-utils>=0.9.0',     # utility library
        'typing;python_version<"3.5"',
        'typing_extensions',
    ],
    py_modules=['walrus'],
    entry_points={
        'console_scripts': [
            'walrus = walrus:main',
        ]
    },
    package_data={
        '': [
            'LICENSE',
            'README.md',
            'CHANGELOG.md',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
