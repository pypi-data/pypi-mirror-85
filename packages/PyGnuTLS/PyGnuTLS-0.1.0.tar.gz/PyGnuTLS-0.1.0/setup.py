#!/usr/bin/python3

import setuptools

setuptools.setup(
    name="PyGnuTLS",
    version="0.1.0",
    description="Python wrapper for the GnuTLS library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="LGPL",
    url="https://github.com/hughsie/PyGnuTLS",
    packages=setuptools.find_packages(),
    author="Richard Hughes",
    author_email="richard@hughsie.com",
    platforms=["Platform Independent"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.5',
)
