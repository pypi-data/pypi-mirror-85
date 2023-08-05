#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: AIIT
# Mail: zhangjun_dlut@outlook.com
# Created Time:  2020-11-10 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="AIITNLP",
    version="0.3.0",
    keywords=("pip", "Ner", "bidding"),
    description="Ner for bidding",
    long_description="time and path tool",
    license="MIT Licence",

    url="https://github.com/choushun/AIITNLP",
    author="AIIT",
    author_email="zhangjun_dlut@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['jieba', 'cpca']
)

