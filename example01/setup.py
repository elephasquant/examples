import os
import sys
from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext


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


if __name__ == '__main__':
    files = list_files("./", "./")
    exts = list(map(lambda x: Extension(x[0], sources=[x[1]]), files))
    print(files)
    setup(
        cmdclass={'build_ext': build_ext},
        ext_modules=exts
    )
