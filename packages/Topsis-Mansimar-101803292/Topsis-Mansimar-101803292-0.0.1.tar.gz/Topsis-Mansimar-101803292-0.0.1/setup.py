import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Mansimar-101803292",
    version="0.0.1",
    description = 'This package can be used to calculate the topsis score of multiple component data and rank them accordingly',   
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mansimar Anand",
    author_email="anandmansimar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['pandas'],
)