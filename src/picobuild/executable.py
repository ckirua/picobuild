import subprocess
import sysconfig
from typing import Optional

from Cython.Compiler import Options as CythonOptions
from Cython.Compiler.Main import compile as cython_compile
from Cython.Compiler.Options import CompilationOptions

# pylint: disable=pointless-string-statement
"""
# TODO
*Cython*
This is embedded, doesnt require env activation to be run.
TODO:
    - cythonize is better option i think
    - maebe a class CythonExecutable with methods:
        - build
        - compile
    - add moar args

*C*
Issa not embedded, activate env to run.
TODO:
    - c file generator
    - compile (think is same as cython)

*Impl*
    - shall i clean cy/c files after executable is done? idkidk
"""


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

    def as_tuple(self):
        """
        Return the source file and executable name as a tuple.
        """
        return (self._source_file, self._executable_file)


def _cythonize_executable(source_file: str, dest_file: str = None):
    """
    Cythonize the source_file to a C file suitable for embedding in a standalone executable.
    Equivalent to: cython --embed hello.py -o bin/hello_cy.c
    """
    # This is equivalent to --embed
    CythonOptions.embed = "main"

    options = CompilationOptions()
    if dest_file:
        options.output_file = dest_file

    cython_compile(source_file, options)


def _build_cython_executable(c_file: str, dest_file: str):
    """
    Compile the C file to an executable using gcc.
    Equivalent to: gcc bin/hello_cy.c -o bin/hello_cy \
       $(python -c "import sysconfig as s; print(f'-I{s.get_path(\"include\")} -L{s.get_config_var(\"LIBDIR\")} -lpython{s.get_config_var(\"VERSION\")}')")
    """
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


def build_cython_executable(source_file: str, dest_file: str = None):
    """
    Build a standalone executable from a Python source file.

    Args:
        source_file: Python source file (e.g., "hello.py")
        dest_file: Output executable path (e.g., "hello"). If None, derived from source_file.
    """
    if dest_file is None:
        dest_file = source_file.removesuffix(".py")

    c_file = f"{dest_file}.c"

    _cythonize_executable(source_file, c_file)
    _build_cython_executable(c_file, dest_file)
