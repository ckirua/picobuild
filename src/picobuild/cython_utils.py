"""Cython build directory helper and cythonize wrapper."""

import platform
import sys
from typing import Any

from Cython.Build import cythonize as _cythonize
from setuptools import Extension


def get_cython_build_dir(build_dir: str = "build") -> str:
    """Return a platform- and Python-specific Cython build directory.

    Keeps Cython-generated files (e.g. .c) separate from the main build tree.
    Example: ``build/cython.linux-x86_64-cpython-313``.

    Args:
        build_dir: Top-level build directory. Default is ``"build"``.

    Returns:
        Path like ``{build_dir}/cython.{platform}-{machine}-{impl}-{py_version}``.
    """
    plat = platform.system().lower()
    machine = platform.machine().lower()
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    impl = platform.python_implementation().lower()
    return f"{build_dir}/cython.{plat}-{machine}-{impl}-{py_version}"


def cythonize(*args: Any, **kwargs: Any) -> list[Extension]:
    """Compile Cython sources into extension modules, using a dedicated build dir.

    Forwards to Cython's cythonize, with ``build_dir`` set via
    ``get_cython_build_dir(kwargs.pop("build_dir", "build"))`` so Cython
    output does not clash with the main setuptools build.

    Args:
        *args: Passed to Cython's cythonize (e.g. list of Extension).
        **kwargs: Passed to Cython's cythonize; ``build_dir`` is consumed
            and replaced by the result of get_cython_build_dir.

    Returns:
        List of setuptools Extension objects ready for ext_modules.
    """
    build_dir: str = kwargs.pop("build_dir", "build")
    return _cythonize(*args, **kwargs, build_dir=get_cython_build_dir(build_dir))
