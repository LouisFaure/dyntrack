from . import __file__

def hello():
    print("helloooooo")

def check_vfkm():
    import os
    from glob import glob
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(glob(os.path.join(basedir,'*.so')))
