#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from os import path

repo_base_dir = path.abspath(path.dirname(__file__))

with open(path.join(repo_base_dir, 'VERSION')) as version_file:
    version = version_file.read().strip()

# Long description
readme = path.join(repo_base_dir, 'README.md')
with open(readme) as f:
    long_description = f.read()

setup(
    name='pandoc-import-code',
    version=version,
    description='Yet another pandoc filter to include external code files.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Noël Macé',
    author_email='contact@noelmace.com',
    license='MIT',
    url='https://github.com/noelmace/pandoc-import-code',

    install_requires=['panflute>=2,<3', 'comment_parser>=1,<2'],
    # Add to lib so that it can be included
    py_modules=['pandoc_import_code'],
    entry_points={
        'console_scripts': [
            'pandoc-import-code=pandoc_import_code:main'
        ]
    },

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ]
)
