"""Re-exports of setuptools Extension, find_packages, and setup for use with Cython builds."""

from typing import Any, Callable, TypeAlias

from setuptools import Extension as _Extension
from setuptools import find_packages as _find_packages
from setuptools import setup as _setup

Extension: TypeAlias = _Extension
"""Alias for setuptools.Extension; use for Cython/C extension modules."""

find_packages: Callable[..., list[str]] = _find_packages
"""Alias for setuptools.find_packages."""

setup: Callable[..., Any] = _setup
"""Alias for setuptools.setup."""