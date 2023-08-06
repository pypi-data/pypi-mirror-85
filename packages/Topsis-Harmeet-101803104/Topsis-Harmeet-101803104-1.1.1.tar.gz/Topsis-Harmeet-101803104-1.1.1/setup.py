import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Harmeet-101803104",
    version="1.1.1",
    description="Implements Topsis",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Harmeet Singh",
    author_email="oberoisahil200@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['pandas'],
)