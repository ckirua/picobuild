# picobuild

Building tools for CPython extensions (Cython, setuptools) and standalone executables.

## Install

```bash
pip install picobuild
```

Or with uv:

```bash
uv add picobuild
```

## Quick start

### setuptools + Cython

Re-export of setuptools’ `Extension`, `find_packages`, and `setup`, plus a Cython build dir that stays out of the way of the main build:

```python
from Cython.Build import cythonize  # or use picobuild.cythonize
from picobuild import Extension, get_cython_build_dir, setup

extensions = cythonize(
    [Extension("mypkg.foo", ["src/mypkg/foo.pyx"])],
    build_dir=get_cython_build_dir(),
)
setup(ext_modules=extensions, ...)
```

Or use picobuild’s `cythonize`, which sets the build dir for you:

```python
from picobuild import Extension, cythonize, setup

extensions = cythonize([Extension("mypkg.foo", ["src/mypkg/foo.pyx"])])
setup(ext_modules=extensions, ...)
```

### Standalone executable from Python

Build a single-file executable from a Python script (Cython --embed + gcc):

```python
from picobuild import build_cython_executable

build_cython_executable("hello.py", "bin/hello")
```

Or with parameters:

```python
from picobuild import ExecutableParameters, build_cython_executable

params = ExecutableParameters("script.py", build_dir="bin", executable_name="myapp")
build_cython_executable(params._source_file, params._executable_file)
```

## API

| Name | Description |
|------|-------------|
| `Extension` | setuptools `Extension` (for Cython/C extensions). |
| `find_packages` | setuptools `find_packages`. |
| `setup` | setuptools `setup`. |
| `get_cython_build_dir(build_dir="build")` | Path like `build/cython.linux-x86_64-cpython-313` for Cython output. |
| `cythonize(*args, **kwargs)` | Cython’s `cythonize` with `build_dir` set via `get_cython_build_dir`. |
| `build_cython_executable(source_file, dest_file=None)` | Build a standalone executable from a `.py` file. |
| `ExecutableParameters(source_file, build_dir, executable_name=None)` | Parameters for the executable build. |

## Docs

Full API and usage: [Sphinx documentation](https://picops.github.io/picobuild/) (or build locally with `make docs`).

## Development

```bash
make sync        # uv sync --extra dev
make install-uv  # sync + editable install
make test        # unittest
make check       # isort, black, flake8, mypy
make docs       # Sphinx HTML in docs/_build/html
```

## License

BSD-3-Clause.
