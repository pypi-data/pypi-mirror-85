"""Setup script for kps"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="kps",
    version="1.0.0",
    description="This is the official kps python module.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/magnumdingusedu/kps",
    author="Vividh Mariya",
    author_email="contact@vmariya.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["kps"],
    include_package_data=True,
    entry_points={"console_scripts": ["kps=kps.__main__:main"]},
)
