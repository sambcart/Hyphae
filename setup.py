from Cython.Build import cythonize
from Cython.Distutils import build_ext

try:
    from setuptools import setup
    from setuptools.extension import Extension

except Exception:
    from distutils.core import setup
    from distutils.extension import Extension

_extra = [ '-O3' , '-ffast-math' ]

exts = [
    Extension('node',
              sources=['./src/node.pyx'],
              extra_compile_args=_extra),
    Extension('root',
              sources=['./src/root.pyx'],
              extra_compile_args=_extra),
    Extension('neighbors',
              sources=['./src/neighbors.pyx'],
              extra_compile_args=_extra)]

setup(
    name = "hyphae",
    install_requires = ["numpy>=1.8.2", "cython>=0.20.0"],
    cmdclass = {"build_ext": build_ext},
    ext_modules = cythonize(exts))
