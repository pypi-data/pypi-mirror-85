#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, Extension
import os,sys,re


with open('README.md', 'r') as fd:
  version = '0.5.1'
  author = 'Ryou Ohsawa'
  email = 'ohsawa@ioa.s.u-tokyo.ac.jp'
  description = 'FDLSGM: Fast Directed Line Segment Grouping Method'
  long_description = fd.read()
  license = 'MIT'


classifiers = [
  'Development Status :: 3 - Alpha',
  'Environment :: Console',
  'Intended Audience :: Science/Research',
  'License :: OSI Approved :: MIT License',
  'Operating System :: POSIX :: Linux',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: Implementation :: CPython',
  'Topic :: Scientific/Engineering :: Astronomy']


if os.path.exists('fdlsgm.pyx'):
  USE_CYTHON = True
  filename   = 'fdlsgm.pyx'
else:
  USE_CYTHON = False
  if os.path.exists('fdlsgm.cpp'):
    filename   = 'fdlsgm.cpp'
  elif os.path.exists('fdlsgm.cxx'):
    filename   = 'fdlsgm.cxx'
  if os.path.exists('fdlsgm.cc'):
    filename   = 'fdlsgm.cc'


if __name__ == '__main__':
  try:
    import numpy
  except ImportError:
    raise SystemExit('NumPy is not available.')

  sources      = [filename] + glob(os.path.join('src', '*.cc'))
  depends      = glob(os.path.join('src', '*.h'))
  libraries    = ['m',]
  include_dirs = [numpy.get_include(), 'src']
  compile_args = ['-std=c++11','-O2']
  extensions   = [
    Extension('fdlsgm',
              language='c++',
              sources=sources,
              libraries=libraries,
              include_dirs=include_dirs,
              depends=depends,
              extra_compile_args=compile_args)
    ]

  if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions, language_level=3)

  setup(
    name='fdlsgm',
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ryou_ohsawa/fdlsgm/src/master/',
    license=license,
    classifiers=classifiers,
    install_requires=['numpy','matplotlib',],
    ext_modules=extensions)
