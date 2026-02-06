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
	@echo "  dist       - sync + build sdist and wheel into dist/ (adds py tag for multi-version)"

dist: sync
	@$(UV) run python -m build --outdir dist
	@py_tag=$$($(UV) run python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"); \
	for f in dist/*.tar.gz; do \
	  [ -f "$$f" ] || continue; \
	  base=$$(basename "$$f" .tar.gz); \
	  case "$$base" in *-py[0-9][0-9][0-9]) continue ;; esac; \
	  mv "$$f" "dist/$${base}-$${py_tag}.tar.gz"; \
	  echo "dist/$${base}-$${py_tag}.tar.gz"; \
	done; \
	for f in dist/*.whl; do \
	  [ -f "$$f" ] || continue; \
	  base=$$(basename "$$f" .whl); \
	  case "$$base" in *-$${py_tag}-*) continue ;; esac; \
	  new=$$(echo "$$base" | sed "s/-py3-/-$${py_tag}-/; s/-cp3[0-9]-cp3[0-9]-/-$${py_tag}-/"); \
	  [ "$$f" = "dist/$$new.whl" ] || { mv "$$f" "dist/$$new.whl"; echo "dist/$$new.whl"; }; \
	done

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
