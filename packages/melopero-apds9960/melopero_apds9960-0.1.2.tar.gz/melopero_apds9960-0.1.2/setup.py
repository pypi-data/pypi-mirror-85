#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""
import setuptools

setuptools.setup(
    name="melopero_apds9960",
    version="0.1.2",
    description="A module to easily access Melopero's APDS9960 sensor's features",
    url="https://github.com/melopero/Melopero_APDS-9960",
    author="Melopero",
    author_email="info@melopero.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    install_requires=["smbus2"],
)
