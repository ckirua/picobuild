UV := uv
PYTHON := python
TEST_DIR := tests
.DEFAULT_GOAL := help

.PHONY: help build clean install test sync install-uv lock dist check

help:
	@echo "picobuild Makefile"
	@echo "  build      - Build Cython extensions in place"
	@echo "  clean      - Clean build and dist"
	@echo "  install    - Install package editable (no-build-isolation)"
	@echo "  test       - Run unit tests"
	@echo "  check      - isort, black, flake8, mypy"
	@echo "  sync       - uv: create venv and install deps (incl. dev)"
	@echo "  install-uv - uv: sync, build, then editable install"
	@echo "  lock       - uv: update uv.lock from pyproject.toml"
	@echo "  dist       - sync + build sdist and wheel into dist/"

dist: sync
	@$(UV) run python -m build --outdir dist

install: sync
	@$(UV) pip install -e . --no-build-isolation

build:
	@$(UV) run $(PYTHON) setup.py build_ext --inplace

clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@find . -type f -name "*.so" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

test:
	@$(UV) run $(PYTHON) -m unittest discover -s $(TEST_DIR) -p "test_*.py" -v

check:
	@$(UV) run $(PYTHON) -m isort src --profile black
	@$(UV) run $(PYTHON) -m black src
	@$(UV) run $(PYTHON) -m flake8 src
	@$(UV) run $(PYTHON) -m black --check src
	@$(UV) run $(PYTHON) -m mypy src

sync:
	@$(UV) sync --extra dev

install-uv: sync
	@$(MAKE) build
	@$(UV) pip install -e . --no-build-isolation

lock:
	@$(UV) lock
