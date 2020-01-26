#!/usr/bin/env python

import os
from setuptools import setup

with open('pyriodic/version.py') as version_file:
    exec(version_file.read())

setup(name='pyriodic-structures',
      author='Matthew Spellings',
      author_email='matthew.p.spellings@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      description='Library to list and manipulate well-known 3D structures',
      entry_points={
          'pyriodic_sources': ['standard = pyriodic.unit_cells:load_standard'],
      },
      extras_require={},
      install_requires=[
          'numpy',
      ],
      license='MIT',
      packages=[
          'pyriodic',
      ],
      project_urls={
          'Documentation': 'http://pyriodic.readthedocs.io/',
          'Source': 'https://github.com/klarh/pyriodic'
          },
      python_requires='>=3',
      version=__version__
      )
