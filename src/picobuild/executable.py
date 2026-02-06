"""Build standalone executables from Python sources via Cython --embed and gcc."""

import subprocess
import sysconfig
from typing import Optional

from Cython.Compiler import Options as CythonOptions
from Cython.Compiler.Main import compile as cython_compile
from Cython.Compiler.Options import CompilationOptions


class ExecutableParameters:
    """
    Parameters for building a standalone executable from a Python source file.

    Args:
        source_file: Python source file (e.g., "hello.py")
        build_dir: Output directory for the executable (e.g., "bin")
        executable_name: Name of the executable (e.g., "hello")
    """

    def __init__(
        self, source_file: str, build_dir: str, executable_name: Optional[str] = None
    ):
        """
        Initialize the ExecutableParameters.

        Args:
            source_file: Python source file (e.g., "hello.py")
            build_dir: Output directory for the executable (e.g., "bin")
            executable_name: Name of the executable (e.g., "hello")
        """
        self._build_dir = build_dir

        self._source_file = source_file
        self._executable_name = executable_name or source_file.split("/")[
            -1
        ].removesuffix(".py")
        self._executable_file = f"{self._build_dir}/{self._executable_name}"
        self._c_file = f"{self._build_dir}/{self._executable_name}.c"

    def as_tuple(self) -> tuple[str, str]:
        """Return (source_file, executable_path) for use with build_cython_executable."""
        return (self._source_file, self._executable_file)


def _cythonize_executable(source_file: str, dest_file: Optional[str] = None) -> None:
    """Compile a Python file to C with Cython in embed mode (main entry point)."""
    # This is equivalent to --embed
    CythonOptions.embed = "main"

    options = CompilationOptions()
    if dest_file:
        options.output_file = dest_file

    cython_compile(source_file, options)


def _build_cython_executable(c_file: str, dest_file: str) -> None:
    """Compile the C file to an executable using gcc and the current Python's include/lib."""
    include_dir = sysconfig.get_path("include")
    lib_dir = sysconfig.get_config_var("LIBDIR")
    python_version = sysconfig.get_config_var("VERSION")

    cmd = [
        "gcc",
        c_file,
        "-o",
        dest_file,
        f"-I{include_dir}",
        f"-L{lib_dir}",
        f"-lpython{python_version}",
    ]

    subprocess.run(cmd, check=True)


def build_cython_executable(
    source_file: str, dest_file: Optional[str] = None
) -> None:
    """Build a standalone executable from a Python source file (Cython --embed + gcc).

    Args:
        source_file: Path to the Python source file (e.g. ``"hello.py"``).
        dest_file: Path for the output executable. If None, derived from
            source_file (same basename without .py). A ``.c`` file is created
            alongside the executable during the build.
    """
    if dest_file is None:
        dest_file = source_file.removesuffix(".py")

    c_file = f"{dest_file}.c"

    _cythonize_executable(source_file, c_file)
    _build_cython_executable(c_file, dest_file)
