"""
picobuild: building tools for CPython extensions and standalone executables.

Provides setuptools re-exports (Extension, find_packages, setup), a Cython
build directory helper (get_cython_build_dir, cythonize), and utilities to
build standalone executables from Python sources (build_cython_executable,
ExecutableParameters).
"""

from .__about__ import __version__
from ._setuptools import Extension, find_packages, setup
from .cython_utils import cythonize, get_cython_build_dir
from .executable import ExecutableParameters, build_cython_executable

__all__: tuple[str, ...] = (
    # About
    "__version__",
    # CythonUtils
    "get_cython_build_dir",
    "cythonize",
    # Setuptools
    "Extension",
    "find_packages",
    "setup",
    # Executable
    "build_cython_executable",
    "ExecutableParameters",
)
