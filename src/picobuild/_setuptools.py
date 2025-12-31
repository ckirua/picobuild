from typing import Any, Callable, TypeAlias

from setuptools import Extension as _Extension
from setuptools import find_packages as _find_packages
from setuptools import setup as _setup

Extension: TypeAlias = _Extension
find_packages: Callable[..., list[str]] = _find_packages
setup: Callable[..., Any] = _setup
