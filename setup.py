#!/usr/bin/env python

import setuptools

# [set version]
version = 'v0.0.1'
# [version set]

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rolfs_sphinx_sandbox",
    version=version,
    author="Rolf Verberg",
    author_email="",
    description="Sphinx sandbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rolfverberg/rolfs_sphinx_sandbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='3.10.19',
    install_requires=[
        "asteval==0.9.31",
        "lmfit==1.1.0",
        "matplotlib==3.9.2",
        "nexpy==1.0.9",
        "nexusformat==1.0.6",
        "numpy==1.26.4",
        "pydantic==2.7.3",
        "scipy==1.11.3",
        "sympy==1.12",
    ],
)
