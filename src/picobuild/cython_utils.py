import platform
import sys

from Cython.Build import cythonize as _cythonize
from setuptools import Extension


def get_cython_build_dir(build_dir: str = "build"):
    # Example: build/cython.linux-x86_64-cpython-313
    plat = platform.system().lower()
    machine = platform.machine().lower()
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    impl = platform.python_implementation().lower()
    return f"{build_dir}/cython.{plat}-{machine}-{impl}-{py_version}"


def cythonize(*args, **kwargs) -> list[Extension]:
    return _cythonize(*args, **kwargs, build_dir=get_cython_build_dir())
