import os
import sys
from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from elephas_wheel import bdist_wheel


def list_files(root: str, src: str) -> list:
    root, src = os.path.normpath(root), os.path.normpath(src)
    fs = os.listdir(src)

    if root == '.':
        root = ""
    if src == '.':
        src = ""

    res, pys = [], []
    for f in fs:
        path_src = os.path.join(src, f)
        if os.path.isdir(path_src):
            res += list_files(root, path_src)
        else:
            if path_src.endswith(".py") and src != root:
                module = ".".join(path_src[len(root):-3].split(os.sep))
                pys.append([module, path_src])
    res += pys
    return res


setup(
    name='pkga',
    version='0.0.1',
    author='xitongsys',
    author_email='xitongsys@gmail.com',
    packages=['pkga'],
    cmdclass={'build_ext': build_ext, 'bdist_wheel': bdist_wheel.bdist_wheel},
    ext_modules=list(map(lambda x: Extension(x[0], sources=[x[1]]), list_files("./", "./")))
)
