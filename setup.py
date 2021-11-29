import os
import pathlib
from setuptools import setup, find_packages
import subprocess
from os import path
from setuptools.dist import Distribution

dir = path.abspath(path.dirname(__file__))

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(path.join(dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

from distutils.command.build import build


class CustomBuild(build):
    def run(self):
        build.run(self)
        subprocess.call(["make", "-C", "vfkm"])


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(foo):
        return True


from setuptools.command.install import install


class InstallPlatlib(install):
    def finalize_options(self):
        install.finalize_options(self)
        if self.distribution.has_ext_modules():
            self.install_lib = self.install_platlib


def set_version():
    head = open(path.join(dir, ".git", "HEAD")).readline()
    if head.find("dev") != -1:
        return {
            "template": "{tag}.dev{ccount}",
            "dev_template": "{tag}.dev{ccount}",
            "dirty_template": "{tag}.dev{ccount}",
        }
    else:
        return {"template": "{tag}", "dev_template": "{tag}", "dirty_template": "{tag}"}


setup(
    name="dyntrack",
    version_config=set_version(),
    setup_requires=["setuptools-git-versioning"],
    description="Python package for the study of particle dynamics from 2D tracks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"dyntrack": "dyntrack"},
    url="https://github.com/LouisFaure/DynTrack",
    packages=find_packages(),
    include_package_data=False,
    install_requires=requirements,
    cmdclass={"build": CustomBuild, "install": InstallPlatlib},
    distclass=BinaryDistribution,
)
