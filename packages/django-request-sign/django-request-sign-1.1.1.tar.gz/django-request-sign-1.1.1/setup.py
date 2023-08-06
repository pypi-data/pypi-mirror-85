# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/12 1:39 下午
@desc:
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-request-sign",
    version="1.1.1",
    author="liyao",
    author_email="liyao2598330@126.com",
    description="django request signature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liyao2598330/django-request-sign",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
)
