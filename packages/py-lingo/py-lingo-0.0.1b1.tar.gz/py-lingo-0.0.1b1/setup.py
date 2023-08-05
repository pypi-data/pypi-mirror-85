from setuptools import setup
from setuptools import find_packages

from pylingo import __version__

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="py-lingo",
    version=__version__,
    description="Utilities for saving Scikit-Learn Linear Models in HDF5 format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Douthwaite",
    author_email="mark@douthwaite.io",
    url="https://github.com/markdouthwaite/py-lingo",
    license="MIT",
    install_requires=["numpy==1.19.2", "h5py==2.10.0", "scikit-learn==0.23.2"],
    extras_require={"tests": ["pytest", "black", "isort", "wheel", "setuptools"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
)