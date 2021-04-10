import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().split("\n")


setup(
    name="clsp",
    description="No Description.",
    long_description=read("README.md"),
    author="Taguar258",
    license="MIT",
    version="1.0",
    keywords="",
    url="https://github.com/Taguar258/clsp",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements("requirements.txt"),
    classifiers=["License :: OSI Approved :: MIT License"],
)
