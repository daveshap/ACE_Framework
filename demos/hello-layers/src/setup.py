from setuptools import find_packages, setup
import re
from os import path

FILE_DIR = path.dirname(path.abspath(path.realpath(__file__)))

with open(path.join(FILE_DIR, "README.md")) as f:
    long_description = f.read()

with open(path.join(FILE_DIR, "requirements.txt")) as f:
    install_requirement = f.readlines()

with open(path.join(FILE_DIR, "ace", "version.py")) as f:
    version = re.match(r'^__version__ = "([\w\.]+)"$', f.read().strip())[1]

setup(
    name="hello-layers",
    version=version,
    author="Chad Phillips",
    author_email="xxx@example.com",
    description="Hello Layers! ACE Demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daveshap/ACE_Framework",
    packages=find_packages(),
    package_data={
    },
    install_requires=install_requirement,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
    },
    scripts=[],
)
