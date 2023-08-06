# _*_ coding=utf-8 _*_
__author__  = "8034.com"
__date__    = "2020-04-20"

from setuptools import setup, find_packages
import sys
import os

# 如果是Windows，显示“nt”，如果是Linux，则“posix”
from magicset.__version__ import __VERSION__

setup(
    name="magicset",
    version = __VERSION__,
    author="goblinintree",
    author_email="goblinintree@126.com",
    description="magicset",
    long_description=open("README.md",encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    platforms=["all"],
    license="MIT",
    keywords = ['magicset', 'test'],
    url="https://pypi.org/project/magicset/#description",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
    install_requires=[
    ],
)