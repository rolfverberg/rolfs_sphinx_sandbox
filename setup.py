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
    python_requires='3.12',
    install_requires=[
        "asteval==1.0.8",
        "lmfit==1.3.4",
        "matplotlib==3.10.8",
        "nexpy==2.0.0",
        "nexusformat==2.0.0",
        "numpy==2.3.5",
        "pydantic==2.12.5",
        "scipy==1.16.3",
        "sympy==1.14.0",
    ],
)
