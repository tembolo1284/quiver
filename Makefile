.PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable".PHONY: all install dev test lint format typecheck clean run help

# Configuration
PYTHON := python3

# Default target
all: help

## Installation

install: ## Install quiver in production mode
	$(PYTHON) -m pip install .

dev: ## Install quiver in development mode with all dev dependencies
	$(PYTHON) -m pip install -e ".[dev]"

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

## Help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Library Path:"
	@echo "  libfdpricing.so should be placed in ~/libraries/"
	@echo "  Or set FDPRICING_LIB_PATH environment variable"
