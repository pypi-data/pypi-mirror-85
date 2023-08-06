import pathlib
from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        README = f.read()
    return README

setup(name="TOPSIS-HIMANSHU-101983063",
    version="0.3",
    description="This is code to find topsis score.",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="HIMANSHU - 101983063",
    packages=['TOPSIS-HIMANSHU-101983063'],
    install_requires=[])
