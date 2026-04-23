# Lumen Root Makefile

PYTHON := python
PIP := $(PYTHON) -m pip
RUFF := ruff
MYPY := mypy
PYTEST := pytest

.PHONY: all iso clean test lint packages setup-dev

all: help

setup-dev:
	@echo "Setting up development environment..."
	@$(PIP) install -e lumen_ai/
	@$(PIP) install ruff mypy pytest

iso:
	@echo "Building Lumen ISO..."
	@scripts/build-iso.sh

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf out/ work/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

test:
	@echo "Running unit tests..."
	@$(PYTEST) lumen_ai/

lint:
	@echo "Running linters (ruff, mypy)..."
	@$(RUFF) check .
	@$(MYPY) lumen_ai/

packages:
	@echo "Building Lumen packages..."
	@scripts/build-packages.sh

run-daemon:
	@echo "Starting Lumen AI Daemon..."
	@env PYTHONPATH=. XDG_RUNTIME_DIR=. python lumen_ai/daemon/main.py

run-overlay:
	@echo "Starting Lumen AI Overlay..."
	@env PYTHONPATH=. XDG_RUNTIME_DIR=. python -m lumen_ai.overlay.main

help:
	@echo "Lumen Build System"
	@echo "Usage:"
	@echo "  make setup-dev - Install dev dependencies and editable package"
	@echo "  make iso       - Build the bootable ISO image"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make test      - Run unit tests"
	@echo "  make lint      - Run linters"
	@echo "  make packages  - Build individual lumen-* packages"
