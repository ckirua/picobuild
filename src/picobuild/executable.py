import subprocess
import sysconfig
from pathlib import Path

from Cython.Compiler import Options as CythonOptions
from Cython.Compiler.Main import compile as cython_compile
from Cython.Compiler.Options import CompilationOptions

_PATH_PREAMBLE = """\
import sys as _sys
for _p in {paths!r}:
    if _p not in _sys.path:
        _sys.path.insert(0, _p)
del _sys, _p
"""


def _inject_preamble(source_file: str, paths: list[str]) -> str:
    """
    Create a temporary file with sys.path preamble injected.
    Paths are resolved to absolute paths at build time.
    Returns path to the temp file.
    """
    # Resolve relative paths to absolute at build time
    source_dir = Path(source_file).resolve().parent
    resolved_paths = [str((source_dir / p).resolve()) for p in paths]

    preamble = _PATH_PREAMBLE.format(paths=resolved_paths)
    source_path = Path(source_file)
    content = source_path.read_text()

    # Create temp file in same directory to preserve relative imports
    temp_file = source_path.with_name(f"_pico_{source_path.name}")
    temp_file.write_text(preamble + content)
    return str(temp_file)


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


def build_cython_executable(
    source_file: str,
    dest_file: str = None,
    *,
    paths: list[str] | None = None,
):
    """
    Build a standalone executable from a Python source file.

    Args:
        source_file: Python source file (e.g., "hello.py")
        dest_file: Output executable path (e.g., "hello"). If None, derived from source_file.
        paths: List of paths (relative to source_file) to add to sys.path at runtime.
               These are resolved to absolute paths at build time.
               Example: ["../../picolib/src", "../src"]
    """
    if dest_file is None:
        dest_file = source_file.removesuffix(".py")

    temp_file = None
    actual_source = source_file
    if paths:
        temp_file = _inject_preamble(source_file, paths)
        actual_source = temp_file

    try:
        c_file = f"{dest_file}.c"
        _cythonize_executable(actual_source, c_file)
        _build_cython_executable(c_file, dest_file)
    finally:
        if temp_file:
            Path(temp_file).unlink(missing_ok=True)
