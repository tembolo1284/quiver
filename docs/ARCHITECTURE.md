#
 Quiver Architecture

This document describes the architecture and design decisions for Quiver.
##
 Overview

Quiver is a terminal-based options book application that provides real-time pricing and Greeks calculation using finite difference methods. The application follows a layered architecture with clear separation of concerns.
##
 System Architecture

```

┌─────────────────────────────────────────────────────────────────────────────┐
│                              QUIVER ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   PRESENTATION LAYER (Textual TUI)                                          │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  BookScreen                                                         │   │
│   │  ┌───────────────────────────────────────────────────────────────┐  │   │
│   │  │  PositionsTable                                               │  │   │
│   │  │  ┌──────────┬────────┬────────┬───────┬───────┬───────┬─────┐ │  │   │
│   │  │  │ Symbol   │ Strike │ Expiry │ Price │ Delta │ Gamma │ P&L │ │  │   │
│   │  │  ├──────────┼────────┼────────┼───────┼───────┼───────┼─────┤ │  │   │
│   │  │  │ AAPL C   │ 180    │ Jun 24 │ 12.45 │ 0.62  │ 0.031 │ +2k │ │  │   │
│   │  │  │ SPY P    │ 450    │ Jul 24 │  8.20 │-0.38  │ 0.018 │ -1k │ │  │   │
│   │  │  │ ...      │ ...    │ ...    │ ...   │ ...   │ ...   │ ... │ │  │   │
│   │  │  └──────────┴────────┴────────┴───────┴───────┴───────┴─────┘ │  │   │
│   │  └───────────────────────────────────────────────────────────────┘  │   │
│   │  ┌─────────────────┐  ┌──────────────────────────────────────────┐  │   │
│   │  │  Toolbar        │  │  GreeksPanel (Aggregate)                 │  │   │
│   │  │  [Refresh All]  │  │  Δ: +1,245  Γ: +89  Θ: -456  V: +2,100  │  │   │
│   │  │  [Add Position] │  │                                          │  │   │
│   │  │  [Export]       │  │  Net Premium: $45,230                    │  │   │
│   │  └─────────────────┘  └──────────────────────────────────────────┘  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  DetailScreen (on position select)                                  │   │
│   │  ┌────────────────────────┐  ┌──────────────────────────────────┐   │   │
│   │  │  Option Details        │  │  Full Greeks                     │   │   │
│   │  │  Type: European Call   │  │  Delta:  0.6234                  │   │   │
│   │  │  Strike: 180.00        │  │  Gamma:  0.0312                  │   │   │
│   │  │  Expiry: 2024-06-21    │  │  Theta: -0.0891                  │   │   │
│   │  │  Spot: 185.50          │  │  Vega:   0.4521                  │   │   │
│   │  │  Model: GBM            │  │  Rho:    0.2134                  │   │   │
│   │  └────────────────────────┘  └──────────────────────────────────┘   │   │
│   │  ┌──────────────────────────────────────────────────────────────┐   │   │
│   │  │  P&L Analysis                                                │   │   │
│   │  │  Entry: $10.20  |  Current: $12.45  |  P&L: +$2.25 (+22%)   │   │   │
│   │  └──────────────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Events / Commands
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   DOMAIN LAYER                                                              │
│                                                                             │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐    │
│   │  Book           │    │  Position       │    │  Option             │    │
│   │  ─────────────  │    │  ─────────────  │    │  ─────────────────  │    │
│   │  positions[]    │───▶│  option         │───▶│  option_type (C/P)  │    │
│   │  add_position() │    │  quantity       │    │  style (EU/AM/...)  │    │
│   │  remove()       │    │  entry_price    │    │  strike             │    │
│   │  get_by_id()    │    │  entry_date     │    │  expiry             │    │
│   │  total_greeks() │    │  current_price  │    │  underlying         │    │
│   │  total_pnl()    │    │  greeks         │    │  barrier (optional) │    │
│   └─────────────────┘    │  pnl()          │    └─────────────────────┘    │
│                          └─────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ price(option, params) → PricingResult
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   PRICING LAYER                                                             │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  <<protocol>>                                                     │    │
│   │  PricingEngine                                                    │    │
│   │  ─────────────────────────────────────────────────────────────    │    │
│   │  + price(option, spot, params) → PricingResult                    │    │
│   │  + price_batch(options[], spots[], params[]) → PricingResult[]    │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                          △                                                  │
│                          │ implements                                       │
│   ┌──────────────────────┴────────────────────────────────────────────┐    │
│   │  FDPricingEngine                                                  │    │
│   │  ─────────────────────────────────────────────────────────────    │    │
│   │  - _fdp: FDPricing (CFFI wrapper)                                 │    │
│   │  - grid_params: GridParams                                        │    │
│   │  + price(option, spot, params) → PricingResult                    │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   ┌─────────────────────┐    ┌─────────────────────────────────────────┐   │
│   │  PricingResult      │    │  ModelParams                            │   │
│   │  ─────────────────  │    │  ─────────────────────────────────────  │   │
│   │  price: float       │    │  rate: float                            │   │
│   │  delta: float       │    │  div_yield: float                       │   │
│   │  gamma: float       │    │  vol: float (or vol surface later)      │   │
│   │  theta: float       │    │  model_type: GBM | Heston | SABR | ...  │   │
│   │  vega: float        │    └─────────────────────────────────────────┘   │
│   │  rho: float         │                                                   │
│   └─────────────────────┘                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ fdp.price_european_call(...)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   BINDINGS LAYER (CFFI)                                                     │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  FDPricing (Pythonic Wrapper)                         fdpricing.py│    │
│   │  ─────────────────────────────────────────────────────────────    │    │
│   │  + price_european_call(spot, strike, rate, div, vol, T) → float   │    │
│   │  + price_european_put(...)                                        │    │
│   │  + price_american_call(...)                                       │    │
│   │  + price_barrier_option(...)                                      │    │
│   │  + price_with_greeks(option_type, ...) → PricingResult            │    │
│   │                                                                   │    │
│   │  # Advanced API (context management)                              │    │
│   │  + create_context() → Context                                     │    │
│   │  + solve_pde(ctx, model, option, grid, params) → Result           │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                          │                                                  │
│                          │ calls                                            │
│                          ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  _fdpricing (Raw CFFI)                               _fdpricing.py│    │
│   │  ─────────────────────────────────────────────────────────────    │    │
│   │  ffi = FFI()                                                      │    │
│   │  lib = ffi.dlopen("libfdpricing.so")                              │    │
│   │                                                                   │    │
│   │  # Direct C function access                                       │    │
│   │  lib.fdp_price_european_call(...)                                 │    │
│   │  lib.fdp_context_new()                                            │    │
│   │  lib.fdp_result_get_delta(...)                                    │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ FFI (dlopen)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   NATIVE LAYER (C)                                                          │
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │  libfdpricing.so                                                  │    │
│   │  ─────────────────────────────────────────────────────────────    │    │
│   │                                                                   │    │
│   │  Convenience API:                                                 │    │
│   │    fdp_price_european_call()    fdp_price_american_call()        │    │
│   │    fdp_price_european_put()     fdp_price_american_put()         │    │
│   │    fdp_price_barrier_option()   fdp_price_asian_call()           │    │
│   │                                                                   │    │
│   │  Full API:                                                        │    │
│   │    fdp_context_new()            fdp_grid_new_1d()                │    │
│   │    fdp_model_new_gbm()          fdp_option_new_vanilla()         │    │
│   │    fdp_solver_params_new()      fdp_solve_pde()                  │    │
│   │    fdp_result_get_price()       fdp_result_get_delta()           │    │
│   │                                                                   │    │
│   │  Models: GBM, Heston, SABR, Merton                               │    │
│   │  Options: European, American, Barrier, Asian, Bermudan, Digital  │    │
│   │  Solvers: Explicit, Implicit, Crank-Nicolson, PSOR               │    │
│   │                                                                   │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

```

##
 Data Flow

```

┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   User clicks "Refresh All"                                                 │
│         │                                                                   │
│         ▼                                                                   │
│   BookScreen.action_refresh()                                               │
│         │                                                                   │
│         ▼                                                                   │
│   for position in book.positions:          ◄─── async, in thread pool      │
│       │                                                                     │
│       ▼                                                                     │
│   engine.price(position.option, spot, params)                               │
│       │                                                                     │
│       ▼                                                                     │
│   fdp.price_european_call(spot, strike, ...)  ─── CFFI call (~200ns)       │
│       │                                                                     │
│       ▼                                                                     │
│   libfdpricing.so executes FD solver          ─── Heavy lifting (~5ms)     │
│       │                                                                     │
│       ▼                                                                     │
│   PricingResult(price, delta, gamma, ...)                                   │
│       │                                                                     │
│       ▼                                                                     │
│   position.update(result)                                                   │
│       │                                                                     │
│       ▼                                                                     │
│   UI refreshes table                                                        │
│                                                                             │
│   Total time for 30 positions: ~150-300ms (feels instant)                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

```

##
 Layer Responsibilities

###
 Presentation Layer (UI)

**
Purpose
**
: Handle user interaction and display
-
 
**
BookScreen
**
: Main view showing positions table and aggregate Greeks
-
 
**
DetailScreen
**
: Deep-dive view for a single position
-
 
**
Widgets
**
: Reusable components (PositionsTable, GreeksPanel, Toolbar)
**
Key Principles
**
:
-
 No business logic in UI components
-
 Async operations for pricing to keep UI responsive
-
 Textual CSS (TCSS) for styling separation
###
 Domain Layer

**
Purpose
**
: Core business entities and rules
-
 
**
Option
**
: Immutable specification of an option contract
-
 
**
Position
**
: Mutable state tracking a held option with quantity and P&L
-
 
**
Book
**
: Aggregate root managing a collection of positions
**
Key Principles
**
:
-
 Pure Python, no external dependencies
-
 Rich domain model with behavior (not anemic data classes)
-
 Immutable where possible (Option), mutable where necessary (Position)
###
 Pricing Layer

**
Purpose
**
: Abstract pricing computations
-
 
**
PricingEngine
**
: Protocol defining the pricing interface
-
 
**
FDPricingEngine
**
: Implementation using fdpricing library
-
 
**
PricingResult
**
: Value object containing price and Greeks
-
 
**
ModelParams
**
: Parameters for the pricing model
**
Key Principles
**
:
-
 Protocol-based design allows swapping implementations
-
 Engine is stateless (thread-safe)
-
 Batch pricing support for efficiency
###
 Bindings Layer

**
Purpose
**
: Bridge Python and C
-
 
**
_fdpricing.py
**
: Raw CFFI bindings (auto-generated)
-
 
**
fdpricing.py
**
: Pythonic wrapper with error handling
**
Key Principles
**
:
-
 Thin wrapper over C API
-
 Handle memory management via 
`ffi.gc()`

-
 Convert C errors to Python exceptions
##
 Key Design Decisions

|
 Decision 
|
 Rationale 
|

|
----------
|
-----------
|

|
 
**
Protocol for PricingEngine
**
 
|
 Allows swapping in Monte Carlo, analytical, or mock engines 
|

|
 
**
Pythonic wrapper over raw CFFI
**
 
|
 Clean API for callers, hides FFI complexity 
|

|
 
**
Domain layer separate from pricing
**
 
|
 Book/Position logic is independent of pricing method 
|

|
 
**
Async pricing in thread pool
**
 
|
 UI stays responsive during "Refresh All" 
|

|
 
**
TCSS for styling
**
 
|
 Keeps presentation concerns out of Python code 
|

|
 
**
Immutable Option, mutable Position
**
 
|
 Options are contracts (fixed), positions change over time 
|


##
 Threading Model

```

┌─────────────────────────────────────────────────────────────────┐
│  Main Thread (Textual Event Loop)                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  UI Events                                               │   │
│  │  - Key presses                                           │   │
│  │  - Mouse clicks                                          │   │
│  │  - Table selection                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         │ post_message() / call_later()         │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  UI Updates                                              │   │
│  │  - Refresh table data                                    │   │
│  │  - Update Greeks panel                                   │   │
│  │  - Show loading indicators                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ run_in_executor()
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Thread Pool (concurrent.futures)                               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Worker 1    │  │  Worker 2    │  │  Worker 3    │          │
│  │  price(opt1) │  │  price(opt2) │  │  price(opt3) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│                           ▼                                     │
│                    CFFI calls to                                │
│                    libfdpricing.so                              │
│                    (GIL released)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

##
 Future Extensions

```

┌─────────────────────────────────────────────────────────────────────────────┐
│                           FUTURE EXTENSIONS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────┐                                                       │
│   │  Market Data    │  REST/WebSocket adapters for live spots, vols        │
│   │  Adapters       │  Yahoo Finance, IBKR, Polygon, etc.                  │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │  Vol Surface    │  Term structure, smile interpolation                 │
│   │  Module         │  SABR calibration                                    │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │  Scenario       │  What-if analysis, stress testing                    │
│   │  Analysis       │  Greeks ladder, P&L attribution                      │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │  Monte Carlo    │  Integrate MC library for exotics                    │
│   │  Engine         │  Path-dependent options                              │
│   └─────────────────┘                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

```
