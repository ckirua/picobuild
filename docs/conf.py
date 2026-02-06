# picobuild documentation
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Multi-version docs: set by CI (CURRENT_DOC_VERSION, DOC_VERSIONS, GITHUB_PAGES_BASE)
_current = os.environ.get("CURRENT_DOC_VERSION", "latest")
_versions = os.environ.get("DOC_VERSIONS", "latest").strip().split(",")
_doc_base = os.environ.get("GITHUB_PAGES_BASE", "")

project = "picobuild"
copyright = "picobuild authors"
author = "ckirua"

# Prefer package version when building from repo (multi-version docs)
try:
    from picobuild.__about__ import __version__
    release = __version__
    version = ".".join(__version__.split(".")[:2])  # X.Y
except ImportError:
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

html_theme = "sphinx_rtd_theme"
html_static_path = []
html_title = "picobuild"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
}
html_show_sphinx = False
html_show_copyright = True
html_context = {
    "current_version": _current,
    "doc_versions": [v.strip() for v in _versions if v.strip()],
    "doc_base": _doc_base.rstrip("/"),
}
html_sidebars = {
    "**": ["version_switcher.html", "localtoc.html", "relations.html", "sourcelink.html", "searchbox.html"],
}

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
