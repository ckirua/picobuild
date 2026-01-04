from .__about__ import __version__
from ._setuptools import Extension, find_packages, setup
from .cython_utils import get_cython_build_dir, cythonize

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
)
