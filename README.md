# quiver

> Terminal-based options book with finite difference pricing and Greeks

A TUI application for managing options positions, powered by high-performance finite difference pricing via [fdpricing](https://github.com/yourusername/fdpricing).

## Features

- **Position Management**: Track your options book with entry prices, quantities, and P&L
- **Real-time Pricing**: Price options using finite difference methods (GBM, Heston, SABR, Merton)
- **Full Greeks**: Delta, Gamma, Theta, Vega, Rho computed via finite differences
- **Aggregate Risk**: Book-level Greeks and net exposure at a glance
- **Multiple Option Types**: European, American, Barrier, Asian, Bermudan, Digital

## Quick Start

```bash
# Clone and install
git clone https://github.com/yourusername/quiver.git
cd quiver

# Install in dev mode
make dev

# Run the TUI
make run
```

## Screenshots

```
┌─ Positions ─────────────────────────────────────────────────────────┐
│ Symbol     Strike   Expiry      Qty    Price    Delta   Gamma   P&L │
│ AAPL C     180.00   2024-06-21   10   $12.45    0.62    0.031  +2.2k│
│ SPY P      450.00   2024-07-19   -5    $8.20   -0.38    0.018  -1.1k│
│ NVDA C     900.00   2024-06-21    5   $45.30    0.71    0.012  +3.5k│
├─────────────────────────────────────────────────────────────────────┤
│ Book Greeks:  Δ +1,245   Γ +89   Θ -456   V +2,100                  │
│ Net Premium: $45,230    Day P&L: +$4,600                            │
└─────────────────────────────────────────────────────────────────────┘
[R]efresh All  [A]dd Position  [D]elete  [E]xport  [Q]uit
```

## Requirements

- Python 3.10+
- libfdpricing.so (built from fdpricing)

## Installation

### 1. Build fdpricing Library

Build the fdpricing library separately and place `libfdpricing.so` in:

```bash
~/libraries/libfdpricing.so
```

Or set the environment variable:

```bash
export FDPRICING_LIB_PATH=/path/to/libfdpricing.so
```

### 2. Install quiver

```bash
cd quiver

# Install with dev dependencies
make dev

# Or production install
make install
```

## Usage

### Running the TUI

```bash
# Start with default (empty) book
make run

# Or directly
quiver

# Load positions from file
quiver --book data/sample_book.json

# Specify custom library path
quiver --lib-path /custom/path/libfdpricing.so
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `r` | Refresh all prices |
| `a` | Add new position |
| `d` | Delete selected position |
| `e` | Export book to JSON |
| `Enter` | View position details |
| `q` | Quit |

## Configuration

Create `~/.config/quiver/config.toml`:

```toml
[pricing]
n_space = 200          # Spatial grid points
n_time = 100           # Time steps
grid_type = "sinh"     # uniform, sinh, log

[model]
default_rate = 0.05    # Risk-free rate
default_div = 0.02     # Dividend yield

[display]
refresh_on_select = true
show_aggregate_greeks = true
```

## Library Search Order

The application searches for `libfdpricing.so` in this order:

1. `FDPRICING_LIB_PATH` environment variable
2. `~/libraries/libfdpricing.so` (primary default)
3. `./lib/libfdpricing.so` (project local)
4. `/usr/local/lib/libfdpricing.so`
5. `/usr/lib/libfdpricing.so`

## Development

```bash
# Run tests
make test

# Run linter
make lint

# Format code
make format

# Type check
make typecheck

# Run all checks
make check
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

```
┌────────────────────────────────────┐
│  TUI (Textual)                     │
│  - BookScreen, DetailScreen        │
│  - PositionsTable, GreeksPanel     │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Domain Layer                      │
│  - Book, Position, Option          │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Pricing Layer                     │
│  - PricingEngine protocol          │
│  - FDPricingEngine                 │
└──────────────┬─────────────────────┘
               │ CFFI
               ▼
┌────────────────────────────────────┐
│  libfdpricing.so                   │
│  - Finite difference solvers       │
│  - GBM, Heston, SABR, Merton       │
└────────────────────────────────────┘
```

## Related Projects

- [fdpricing](https://github.com/yourusername/fdpricing) - The underlying C pricing library
