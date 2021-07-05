import os
import pathlib
from setuptools import setup, find_packages
import subprocess
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

from distutils.command.build import build


class CustomBuild(build):
    def run(self):
        build.run(self)
        subprocess.call(["make", "-C", "vfkm"])


setup(
    name="dyntrack",
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}",
        "dirty_template": "{tag}",
    },
    setup_requires=["setuptools-git-versioning"],
    description="Python package for the study of particle dynamics from 2D tracks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"dyntrack": "dyntrack"},
    url="https://github.com/LouisFaure/DynTrack",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    cmdclass={
        "build": CustomBuild,
    },
)
