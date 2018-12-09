#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="kovot",
    packages=["kovot", "kovot.stream"],
    install_requires=[
        "slackclient>=1.2.1"
    ],
    version="0.1.0",
    author="kenkov",
    author_email="kenkovtan@gmail.com",
    url="http://kenkov.jp",
)
