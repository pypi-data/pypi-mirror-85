# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:53:21 2020

@author: Zwenex
"""

from setuptools import setup, find_packages

classifiers =[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
        
        ]
setup(
      name='mark_libray',
      version='0.0.1',
      description='format table',
      long_description=open('readme.txt').read()+'\n\n' + open('CHANGELOG.txt').read(),
      url='',
      author='Thiri Bhone',
      author_email='thiribhonemyintaung@gmail.com',
      license='MIT',
      classifiers=classifiers,
      keywords='mark',
      packages=find_packages(),
      install_requires=['']
      
      
      )