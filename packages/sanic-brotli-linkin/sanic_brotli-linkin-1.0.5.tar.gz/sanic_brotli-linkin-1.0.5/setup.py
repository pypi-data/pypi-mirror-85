#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    @author     :   xstatus
    @time       :   2020/11/15 16:43
    @email      :   crawler@88.com
    @project    :   sanic_brotli -> setup.py
    @IDE        :   PyCharm
    @describe   :   ooops
"""

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="sanic_brotli-linkin", # Replace with your own username
    version="1.0.5",
    author="linkin",
    author_email="crawler@88.com",
    description="Brotli Compression ALg. on Sanic responses.",
    long_description_content_type="text/markdown",
    url='https://github.com/01ly/sanic_brotli',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)