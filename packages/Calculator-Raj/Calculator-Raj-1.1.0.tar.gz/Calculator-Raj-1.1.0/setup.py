from setuptools import setup
with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(name="Calculator-Raj",
version="1.1.0",
description="This is a simple calculator program",
long_description=long_description,
url='https://test.pypi.org/legacy/',
author="Rajeev Singla",
packages=['calci_raj'],
include_package_data=True,
install_requires=[],
classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)

