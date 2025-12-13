#!/usr/bin/env python3
"""Build script for CFFI bindings to libfdpricing.

Run this script to regenerate _fdpricing.py:
    python src/quiver/bindings/build_ffi.py
"""

from cffi import FFI

# C declarations for the fdpricing library
CDEF = """
// Error codes
typedef enum {
    FDP_OK = 0,
    FDP_ERROR_NULL_POINTER,
    FDP_ERROR_INVALID_PARAM,
    FDP_ERROR_ALLOCATION,
    FDP_ERROR_CONVERGENCE,
    FDP_ERROR_NOT_IMPLEMENTED,
    FDP_ERROR_STABILITY,
    FDP_ERROR_BOUNDS
} fdp_error_t;

// Opaque types
typedef struct fdp_context fdp_context_t;
typedef struct fdp_grid fdp_grid_t;
typedef struct fdp_model fdp_model_t;
typedef struct fdp_option fdp_option_t;
typedef struct fdp_solver_params fdp_solver_params_t;
typedef struct fdp_result fdp_result_t;

// Grid types
typedef enum {
    FDP_GRID_UNIFORM = 0,
    FDP_GRID_SINH,
    FDP_GRID_LOG
} fdp_grid_type_t;

// Option types
typedef enum {
    FDP_OPTION_CALL = 0,
    FDP_OPTION_PUT
} fdp_option_type_t;

// Option styles
typedef enum {
    FDP_STYLE_EUROPEAN = 0,
    FDP_STYLE_AMERICAN,
    FDP_STYLE_BERMUDAN
} fdp_style_t;

// Solver methods
typedef enum {
    FDP_SOLVER_EXPLICIT = 0,
    FDP_SOLVER_IMPLICIT,
    FDP_SOLVER_CRANK_NICOLSON,
    FDP_SOLVER_PSOR
} fdp_solver_method_t;

// Barrier types
typedef enum {
    FDP_BARRIER_UP_AND_IN = 0,
    FDP_BARRIER_UP_AND_OUT,
    FDP_BARRIER_DOWN_AND_IN,
    FDP_BARRIER_DOWN_AND_OUT
} fdp_barrier_type_t;

// Convenience API - European options
double fdp_price_european_call(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_european_put(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

// Convenience API - American options
double fdp_price_american_call(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_american_put(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

// Convenience API - Barrier options
double fdp_price_barrier_option(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, double barrier,
    fdp_option_type_t option_type, fdp_barrier_type_t barrier_type,
    int n_space, int n_time
);

// Convenience API - Asian options
double fdp_price_asian_call(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_asian_put(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

// Convenience API - Bermudan options
double fdp_price_bermudan_call(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_exercise_dates,
    int n_space, int n_time
);

double fdp_price_bermudan_put(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_exercise_dates,
    int n_space, int n_time
);

// Convenience API - Digital options
double fdp_price_digital_call(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_digital_put(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

// Convenience API - Lookback options
double fdp_price_lookback_call_floating(
    double spot, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_lookback_put_floating(
    double spot, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_lookback_call_fixed(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

double fdp_price_lookback_put_fixed(
    double spot, double strike, double rate, double div_yield,
    double vol, double maturity, int n_space, int n_time
);

// Full API - Context management
fdp_context_t* fdp_context_new(void);
void fdp_context_free(fdp_context_t* ctx);
fdp_error_t fdp_context_get_error(fdp_context_t* ctx);
const char* fdp_error_string(fdp_error_t err);

// Full API - Grid
fdp_grid_t* fdp_grid_new_1d(
    fdp_context_t* ctx, fdp_grid_type_t type,
    int n_space, int n_time, double spot,
    double s_min, double s_max, double maturity
);
void fdp_grid_free(fdp_grid_t* grid);

// Full API - Model
fdp_model_t* fdp_model_new_gbm(
    fdp_context_t* ctx, double rate, double div_yield, double vol
);
void fdp_model_free(fdp_model_t* model);

// Full API - Option
fdp_option_t* fdp_option_new_vanilla(
    fdp_context_t* ctx, fdp_option_type_t type,
    fdp_style_t style, double strike, double maturity
);
void fdp_option_free(fdp_option_t* option);

// Full API - Solver
fdp_solver_params_t* fdp_solver_params_new(fdp_context_t* ctx);
void fdp_solver_params_set_method(fdp_solver_params_t* params, fdp_solver_method_t method);
void fdp_solver_params_free(fdp_solver_params_t* params);

// Full API - Solve
fdp_result_t* fdp_solve_pde(
    fdp_context_t* ctx, fdp_model_t* model,
    fdp_option_t* option, fdp_grid_t* grid,
    fdp_solver_params_t* params
);

// Full API - Results
double fdp_result_get_price(fdp_result_t* result, double spot);
double fdp_result_get_delta(fdp_result_t* result, double spot);
double fdp_result_get_gamma(fdp_result_t* result, double spot);
double fdp_result_get_theta(fdp_result_t* result, double spot);
void fdp_result_free(fdp_result_t* result);
"""


def build_ffi() -> FFI:
    """Build and return the FFI object."""
    ffi = FFI()
    ffi.cdef(CDEF)
    return ffi


def main() -> None:
    """Generate the bindings module."""
    import sys
    from pathlib import Path

    # Build FFI
    ffi = build_ffi()

    # Write the generated file
    output_dir = Path(__file__).parent
    output_file = output_dir / "_fdpricing_ffi.py"

    # For ABI mode, we just need to save the cdef
    # The actual loading happens at runtime in fdpricing.py
    print(f"CFFI definitions ready. Use FDPricing class from fdpricing.py")
    print(f"Library will be loaded at runtime via ffi.dlopen()")


if __name__ == "__main__":
    main()
