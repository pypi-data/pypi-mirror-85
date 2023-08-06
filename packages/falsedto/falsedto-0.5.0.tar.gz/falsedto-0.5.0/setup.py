#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, find_packages
from setuptools import Extension
import os,sys,re


with open('README.md', 'r') as fd:
  version = '0.5.0'
  author = 'Ryou Ohsawa'
  email = 'ohsawa@ioa.s.u-tokyo.ac.jp'
  description = 'falsedto: Faint Line Segment Detection Tool'
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
  'Topic :: Scientific/Engineering :: Astronomy']


USE_CYTHON = False

def get_filename(name):
  if os.path.exists('src/{}.pyx'.format(name)):
    USE_CYTHON = True
    return ['src/{}.pyx'.format(name),]
  else:
    USE_CYTHON = False
    if os.path.exists('src/{}.cpp'.format(name)):
      filename = ['src/{}.cpp'.format(name),]
    elif os.path.exists('src/{}.cxx'.format(name)):
      filename = ['src/{}.cxx'.format(name),]
    elif os.path.exists('src/{}.cc'.format(name)):
      filename = ['src/{}.cc'.format(name),]
    else:
      raise RuntimeError('no file matches name "{}"'.format(name))


if __name__ == '__main__':
  try:
    import numpy
  except ImportError:
    raise SystemExit('NumPy is not available.')


  depends      = glob(os.path.join('src','*.h'))
  libraries    = ['m',]
  include_dirs = [numpy.get_include(), 'src']
  link_args    = ['-fopenmp']
  compile_args = ['-std=c++11','-O2','-fopenmp']

  ext_modules = [
    Extension(
      'falsedto.hough', language='c++', sources=get_filename('hough'),
      libraries=libraries, include_dirs=include_dirs,
      depends=depends, extra_link_args=link_args,
      extra_compile_args=compile_args),
  ]

  if USE_CYTHON:
    from Cython.Build import cythonize
    ext_modules = cythonize(ext_modules, language_level=3)

  setup(
    name='falsedto',
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ryou_ohsawa/falsedt/src/master/',
    license=license,
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=['numpy','matplotlib','sep'],
    ext_modules=ext_modules)
