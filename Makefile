.PHONY: all install dev test lint format typecheck clean run help

PYTHON := python3

all: help

install:
	$(PYTHON) -m pip install .

dev:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) -m quiver

run-dev:
	textual run --dev src/quiver/app.py

run-sample:
	$(PYTHON) -m quiver --book data/sample_book.json

test:
	$(PYTHON) -m pytest tests/ -v

test-fast:
	$(PYTHON) -m pytest tests/ -v --no-cov

test-unit:
	$(PYTHON) -m pytest tests/ -v -m "not integration"

test-bindings:
	$(PYTHON) -m pytest tests/test_bindings.py -v

lint:
	$(PYTHON) -m ruff check src/ tests/

lint-fix:
	$(PYTHON) -m ruff check --fix src/ tests/

format:
	$(PYTHON) -m black src/ tests/

format-check:
	$(PYTHON) -m black --check src/ tests/

typecheck:
	$(PYTHON) -m mypy src/quiver/

check: lint typecheck test

clean:
	rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install     Install quiver"
	@echo "  dev         Install in development mode"
	@echo "  run         Run the TUI"
	@echo "  run-sample  Run with sample book"
	@echo "  test        Run tests"
	@echo "  lint        Run linter"
	@echo "  format      Format code"
	@echo "  typecheck   Run type checker"
	@echo "  clean       Remove build artifacts"
	@echo ""
	@echo "Library: Place libfdpricing.so in ~/libraries/"
