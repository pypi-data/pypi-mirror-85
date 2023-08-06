import pathlib
from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        README = f.read()
    return README

setup(name="TOPSIS-101803359-ShubhamGupta",
    version="1.2.1",
    description="This is code to find topsis score.",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="Shubham Gupta - 101803359",
    packages=['TOPSIS-101803359-ShubhamGupta'],
    install_requires=[])
