from setuptools import setup
from setuptools.command.build_ext import build_ext
import subprocess

class VfkmBuildExt(build_ext):
    def run(self):
        # Run make command in vfkm directory
        subprocess.check_call(['make', '-C', 'vfkm'])
        super().run()

setup(
    cmdclass={
        'build_ext': VfkmBuildExt,
    }
)
