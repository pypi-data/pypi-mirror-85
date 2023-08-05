# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqtcs",
    version="1.1.1",
    author="chenghaiyuan",
    author_email="334180587@1qq.com",
    description="Python wrapper for qtcs: natural language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'ta_lib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

)
