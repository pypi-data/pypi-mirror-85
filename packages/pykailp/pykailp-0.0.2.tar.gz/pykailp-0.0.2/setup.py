# -*- coding: utf-8 -*-
# @Time    : 2020/8/12-22:08
# @Author  : 贾志凯
# @File    : setup.py
# @Software: win10  python3.6 PyCharm

import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name="pykailp",
    version="0.0.2",
    author="jiazhikai",
    author_email="15716539228@163.com",
    description="Python wrapper for kailp: natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
