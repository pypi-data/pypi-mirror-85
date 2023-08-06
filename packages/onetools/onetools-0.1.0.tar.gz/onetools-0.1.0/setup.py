#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time: 2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="onetools",
    version="0.1.0",
    keywords=("pip", "mysql"),
    description="chandler tool",
    long_description="chandler tool",
    license="MIT Licence",

    url="https://github.com/chandlercjy",
    author="ChandlerChan",
    author_email="chenjiayicjy@126.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
