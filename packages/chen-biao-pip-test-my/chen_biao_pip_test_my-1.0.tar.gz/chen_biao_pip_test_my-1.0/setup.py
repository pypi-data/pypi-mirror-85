# -*- encoding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2020/11/9 21:33
@Author  : biao chen
@Email   : 1259319710@qq.com
@Software: PyCharm
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chen_biao_pip_test_my", # Replace with your own username
    version="1.0",
    author="chen biao",
    author_email="1259319710@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/66chenbiao/pip_test.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["mycv"],
    python_requires='>=3.6',
)