from setuptools import setup
from setuptools.command.install import install
import subprocess
import os
import shutil

class CustomInstall(install):
    def run(self):
        # Create build directories if they don't exist        
        # Run make command in vfkm directory
        subprocess.check_call(['make', '-C', 'vfkm'])
        super().run()

setup(
    cmdclass={
        'install': CustomInstall,
    }
)
