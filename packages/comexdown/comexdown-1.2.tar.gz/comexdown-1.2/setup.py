import codecs
import os.path
import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


name = "comexdown"
version = get_version(os.path.join("comexdown", "__init__.py"))
author = "Daniel Komesu"
author_email = "contact@dkko.me"
description = "A little utility to download Brazil's foreign trade data"
with open("README.md", "r") as fh:
    long_description = fh.read()
url = "https://github.com/dankkom/comexdown"
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Utilities",
]
entry_points = {
    "console_scripts": ["comexdown=comexdown.cli:main"],
}

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=classifiers,
    python_requires=">=3.6",
    entry_points=entry_points,
)
