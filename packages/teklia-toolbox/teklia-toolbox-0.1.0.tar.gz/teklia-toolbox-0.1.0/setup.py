#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

from setuptools import find_packages, setup


def requirements(path):
    assert os.path.exists(path), "Missing requirements {}".format(path)
    with open(path) as f:
        return list(map(str.strip, f.read().splitlines()))


with open("VERSION") as f:
    VERSION = f.read()

install_requires = requirements("requirements.txt")

setup(
    name="teklia-toolbox",
    version=VERSION,
    author="Teklia",
    author_email="contact@teklia.com",
    python_requires=">=3.7",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
)
