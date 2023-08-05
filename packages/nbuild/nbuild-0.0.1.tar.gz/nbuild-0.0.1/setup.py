
# This file is part of the python/pip
# packaging system; see https://packaging.python.org/tutorials/packaging-projects/
# for details.

# To upload a new release of the library developers run:
#   python setup.py sdist bdist_wheel
#   python -m twine upload dist/*

# Upload details may be further automated by putting details
# in a private file at ~/.pypirc, documented at: https://packaging.python.org/specifications/pypirc/

import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbuild",
    version="0.0.1",
    author="Jeffrey McAteer",
    author_email="jeffrey.p.mcateer@gmail.com",
    description="A modern project-as-code specification, build, testing, and report generation library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jeffrey-P-McAteer/nbuild",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

