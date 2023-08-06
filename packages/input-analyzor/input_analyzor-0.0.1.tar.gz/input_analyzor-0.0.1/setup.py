#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="input_analyzor",
    version="0.0.1",
    author="Alex Z",
    author_email="alexchunggh@gmail.com",
    description="Arena mine model input analyzor, working with excel input workbook 116D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.riotinto.org/IOps-Strategy-Simulation-Modelling/Input-Analyzor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)