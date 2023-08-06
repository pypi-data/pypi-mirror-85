#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 16:07
@File    : setup.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as rm:
    long_description = rm.read()
print(find_packages(exclude=[
          'strategies', 'strategies.*', 'Scripts',
          'quant_vnpy.data', 'quant_vnpy.data.*'
      ]))
setup(name='quant_vnpy',
      version='0.1.2',
      description='基于VNPY进行功能增强',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='MG',
      author_email='mmmaaaggg@163.com',
      url='http://192.168.0.103/quant/quant_vnpy',
      packages=find_packages(exclude=[
          'strategies', 'strategies.*', 'Scripts',
          'quant_vnpy.data', 'quant_vnpy.data.*'
      ]),
      python_requires='>=3.6',
      classifiers=(
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.7",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: Unix",
          "Operating System :: POSIX",
          "License :: OSI Approved :: MIT License",
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: Developers",
          "Natural Language :: Chinese (Simplified)",
          "Topic :: Software Development",
      ),
      install_requires=[
          'IBATS_Common>=0.20.8',
          'psutil>=5.7.2',
          'kaleido>=0.0.3',
          'openpyxl>=3.0.5',
          'xlwt>=1.3.0',
      ])
