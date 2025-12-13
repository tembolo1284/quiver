.PHONY: all install dev test lint format typecheck clean bindings run build-fdpricing help

# Configuration
PYTHON := python3
FDPRICING_DIR ?= ../fdpricing
LIB_DIR := lib

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

## Building

bindings: ## Build CFFI bindings for fdpricing
	$(PYTHON) src/quiver/bindings/build_ffi.py

build-fdpricing: ## Build fdpricing library and copy to lib/
	@echo "Building fdpricing from $(FDPRICING_DIR)..."
	@if [ ! -d "$(FDPRICING_DIR)" ]; then \
		echo "Error: fdpricing directory not found at $(FDPRICING_DIR)"; \
		echo "Set FDPRICING_DIR to the correct path"; \
		exit 1; \
	fi
	$(MAKE) -C $(FDPRICING_DIR) build
	@mkdir -p $(LIB_DIR)
	cp $(FDPRICING_DIR)/build/lib/libfdpricing.so $(LIB_DIR)/
	cp $(FDPRICING_DIR)/build/lib/libfdpricing.a $(LIB_DIR)/
	@echo "Libraries copied to $(LIB_DIR)/"

## Running

run: ## Run the quiver TUI
	$(PYTHON) -m quiver

run-dev: ## Run with textual dev console (for debugging)
	textual run --dev src/quiver/app.py

run-sample: ## Run with sample book data
	$(PYTHON) -m quiver --book data/sample_book.json

## Testing

test: ## Run all tests
	$(PYTHON) -m pytest tests/ -v

test-fast: ## Run tests without coverage
	$(PYTHON) -m pytest tests/ -v --no-cov

test-unit: ## Run only unit tests (no integration)
	$(PYTHON) -m pytest tests/ -v -m "not integration"

test-bindings: ## Run only binding tests
	$(PYTHON) -m pytest tests/test_bindings.py -v

## Code Quality

lint: ## Run linter (ruff)
	$(PYTHON) -m ruff check src/ tests/

lint-fix: ## Run linter and auto-fix issues
	$(PYTHON) -m ruff check --fix src/ tests/

format: ## Format code with black
	$(PYTHON) -m black src/ tests/

format-check: ## Check code formatting without changes
	$(PYTHON) -m black --check src/ tests/

typecheck: ## Run type checker (mypy)
	$(PYTHON) -m mypy src/quiver/

check: lint typecheck test ## Run all checks (lint, typecheck, test)

## Cleanup

clean: ## Remove build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -path "*/quiver/*" -delete

clean-lib: ## Remove compiled libraries
	rm -rf $(LIB_DIR)/*.so $(LIB_DIR)/*.a

clean-all: clean clean-lib ## Remove all generated files

## Documentation

docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Environment Variables:"
	@echo "  FDPRICING_DIR   Path to fdpricing repository (default: ../fdpricing)"
