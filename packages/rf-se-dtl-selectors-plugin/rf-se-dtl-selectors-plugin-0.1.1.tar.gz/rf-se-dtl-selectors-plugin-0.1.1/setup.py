#!/usr/bin/env python3

import re
import setuptools

with open("TestingLibrarySelectorsPlugin/_version.py", "r") as f:
    try:
        version = re.search(
            r"__version__\s*=\s*[\"']([^\"']+)[\"']",f.read()).group(1)
    except:
        raise RuntimeError('Version info not available')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rf-se-dtl-selectors-plugin",
    version=version,
    author="Toni Kangas",
    description="DOM testing library inspired selectors for Robot Framework SeleniumLibrary.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangasta/rf-se-dtl-selectors-plugin",
    packages=setuptools.find_packages(),
    install_requires=[
        "robotframework-seleniumlibrary~=4.0",
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
