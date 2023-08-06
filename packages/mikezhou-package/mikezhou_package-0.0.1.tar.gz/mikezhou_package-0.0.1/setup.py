# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : Mike Zhou
# @Email : 公众号：测试开发技术
# @File : setup.py.py
# @Project: 第22课时

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='mikezhou_package',  # 包名
      version='0.0.1',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='mikezhou_talk',
      author_email='762357658@qq.com',
      url='https://github.com/zhoujinjian',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )