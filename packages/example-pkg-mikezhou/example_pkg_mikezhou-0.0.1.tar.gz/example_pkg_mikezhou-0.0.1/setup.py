# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : Mike Zhou
# @Email : 公众号：测试开发技术
# @File : setup.py
# @Project: 第22课时


import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="example_pkg_mikezhou",
  version="0.0.1",
  author="mikezhou_talk",
  author_email="762357658@qq.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/zhoujinjian",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)