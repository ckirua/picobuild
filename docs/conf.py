# picobuild documentation
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

project = "picobuild"
copyright = "picobuild authors"
author = "ckirua"
release = "0.0.4"
version = "0.0.4"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = []
html_title = "picobuild"

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"
napoleon_use_param = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "setuptools": ("https://setuptools.pypa.io/en/stable", None),
    "cython": ("https://cython.readthedocs.io/en/stable", None),
}
