from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='OwnPackage',
  version='0.0.1',
  description='This is a library which calculates the rank by given data.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Roushan Singh',
  author_email='rsingh3_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='Topsis',
  packages=find_packages(),
  install_requires=[''] 
)# -*- coding: utf-8 -*-

