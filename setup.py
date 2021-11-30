from setuptools.command.build_ext import build_ext
import os
import pathlib
from setuptools import setup, find_packages
import subprocess
from os import path

dir = path.abspath(path.dirname(__file__))

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(path.join(dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

from distutils.command.build import build


class custom_build_ext(build_ext):
    def build_extensions(self):
        self.compiler.set_executable("compiler_so", "g++ -O -Wall")
        self.compiler.set_executable("compiler_cxx", "g++ -O -Wall")
        self.compiler.set_executable("linker_so", "g++")
        build_ext.build_extensions(self)


def set_version():
    head = open(path.join(dir, ".git", "HEAD")).readline()
    if head.find("dev") != -1:
        return {
            "template": "{tag}.dev{ccount}",
            "dev_template": "{tag}.dev{ccount}",
            "dirty_template": "{tag}.dev{ccount}",
        }
    elif head.find("main") != -1:
        return {"template": "{tag}", "dev_template": "{tag}", "dirty_template": "{tag}"}


from distutils.core import Extension

module1 = Extension(
    "dyntrack.vfkm",
    sources=[
        "vfkm/main.cpp",
        "vfkm/Vector.cpp",
        "vfkm/PolygonalPath.cpp",
        "vfkm/Vector2D.cc",
        "vfkm/Util.cpp",
        "vfkm/Grid.cpp",
        "vfkm/Optimizer.cpp",
        "vfkm/ConstraintMatrix.cpp",
    ],
    include_dirs=["vfkm/"],
)

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
    ext_modules=[module1],
    cmdclass={"build_ext": custom_build_ext},
)
