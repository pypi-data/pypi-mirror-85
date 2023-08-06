#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

history = ""
requirements = []

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=6",
]

setup(
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Named Data Frames",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="namedframes",
    name="namedframes",
    packages=find_packages(include=["namedframes", "namedframes.*"]),
    setup_requires=setup_requirements,
    extras_require={"pyspark": ["pyspark>=2.4.5"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/bdilday/namedframes",
    version="0.1.2",
    zip_safe=False,
)
