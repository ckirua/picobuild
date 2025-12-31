.DEFAULT_GOAL := help

PYTHON      := python
PIP         := pip
PACKAGES    := picobuild
TEST_DIR    := tests

.PHONY: build clean check help install test

help:
	@echo "Welcome to the Picobuild Makefile"
	@echo "Available commands:"
	@echo "  help    - Show this help message"
	@echo "  build   - Build the package"
	@echo "  clean   - Clean the build and dist directories"
	@echo "  install - Install the package"
	@echo "  test    - Run unit tests"
	@echo "  check   - Check code style, formatting, and type safety"

build:
	@$(PYTHON) setup.py build_ext --inplace

clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@find . -type f -name "*.so" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +

check:
	@echo ""
	@echo "\033[1;36mRunning isort for import organization...\033[0m"
	@$(PYTHON) -m isort src --profile black

	@echo ""
	@echo "\033[1;36mFormatting code with black...\033[0m"
	@$(PYTHON) -m black src

	@echo ""
	@echo "\033[1;36mLinting with flake8...\033[0m"
	@$(PYTHON) -m flake8 src

	@echo ""
	@echo "\033[1;36mChecking code style with black...\033[0m"
	@$(PYTHON) -m black --check src

	@echo ""
	@echo "\033[1;36mType checking with mypy...\033[0m"
	@$(PYTHON) -m mypy src

	@echo ""

install:
	@$(PIP) install -e .

test:
	@$(PYTHON) -m unittest discover -s $(TEST_DIR) -p "test_*.py" -v
