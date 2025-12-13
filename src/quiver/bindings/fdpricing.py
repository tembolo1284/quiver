"""Pythonic wrapper over raw CFFI bindings for libfdpricing.

This module provides a clean Python API over the C library,
handling library loading, error checking, and resource management.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import TYPE_CHECKING

from cffi import FFI

# Import the cdef from build_ffi
from quiver.bindings.build_ffi import CDEF


class FDPricingError(Exception):
    """Exception raised for fdpricing library errors."""

    pass


class FDPricingNotFoundError(FDPricingError):
    """Exception raised when libfdpricing.so cannot be found."""

    pass


class FDPricing:
    """Pythonic wrapper for the fdpricing C library.

    This class provides a clean Python interface to libfdpricing,
    handling library loading and providing convenient methods
    for pricing options.

    Example:
        fdp = FDPricing()
        price = fdp.price_european_call(
            spot=100, strike=100, rate=0.05, div_yield=0.02,
            vol=0.20, maturity=1.0, n_space=200, n_time=100
        )
    """

    # Default search paths for the library
    DEFAULT_LIB_PATHS = [
        # Primary location: ~/libraries/
        Path.home() / "libraries" / "libfdpricing.so",
        # Relative to quiver package (local lib/ directory)
        Path(__file__).parent.parent.parent.parent / "lib" / "libfdpricing.so",
        # System paths
        Path("/usr/local/lib/libfdpricing.so"),
        Path("/usr/lib/libfdpricing.so"),
    ]

    def __init__(self, lib_path: str | Path | None = None) -> None:
        """Initialize the wrapper and load the library.

        Args:
            lib_path: Optional explicit path to libfdpricing.so.
                      If not provided, searches default locations.
                      Primary default: ~/libraries/libfdpricing.so

        Raises:
            FDPricingNotFoundError: If the library cannot be found.
        """
        self._ffi = FFI()
        self._ffi.cdef(CDEF)
        self._lib = self._load_library(lib_path)

    def _load_library(self, lib_path: str | Path | None) -> object:
        """Load the shared library.

        Args:
            lib_path: Optional explicit library path

        Returns:
            Loaded library object

        Raises:
            FDPricingNotFoundError: If library cannot be found
        """
        # If explicit path provided, use it
        if lib_path is not None:
            path = Path(lib_path)
            if not path.exists():
                raise FDPricingNotFoundError(f"Library not found at: {path}")
            return self._ffi.dlopen(str(path))

        # Check environment variable
        env_path = os.environ.get("FDPRICING_LIB_PATH")
        if env_path:
            path = Path(env_path)
            if path.exists():
                return self._ffi.dlopen(str(path))

        # Search default paths
        for path in self.DEFAULT_LIB_PATHS:
            if path.exists():
                return self._ffi.dlopen(str(path))

        # Try system library path (let dlopen search)
        try:
            return self._ffi.dlopen("libfdpricing.so")
        except OSError:
            pass

        # Build helpful error message
        searched = [str(p) for p in self.DEFAULT_LIB_PATHS]
        if env_path:
            searched.insert(0, env_path)
        msg = (
            "Could not find libfdpricing.so. Searched:\n"
            + "\n".join(f"  - {p}" for p in searched)
            + "\n\nPlace libfdpricing.so in ~/libraries/"
            + "\nOr set FDPRICING_LIB_PATH environment variable"
        )
        raise FDPricingNotFoundError(msg)

    def _check_result(self, value: float, operation: str) -> float:
        """Check if result is valid (not NaN).

        Args:
            value: Result from C function
            operation: Description of operation for error message

        Returns:
            The value if valid

        Raises:
            FDPricingError: If result is NaN (indicates error)
        """
        if math.isnan(value):
            raise FDPricingError(f"{operation} failed (returned NaN)")
        return value

    # -------------------------------------------------------------------------
    # Convenience API - European Options
    # -------------------------------------------------------------------------

    def price_european_call(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price a European call option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_european_call(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "European call pricing")

    def price_european_put(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price a European put option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_european_put(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "European put pricing")

    # -------------------------------------------------------------------------
    # Convenience API - American Options
    # -------------------------------------------------------------------------

    def price_american_call(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price an American call option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_american_call(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "American call pricing")

    def price_american_put(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price an American put option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_american_put(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "American put pricing")

    # -------------------------------------------------------------------------
    # Convenience API - Barrier Options
    # -------------------------------------------------------------------------

    def price_barrier_option(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        barrier: float,
        is_call: bool = True,
        is_up: bool = True,
        is_knock_in: bool = True,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price a barrier option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            barrier: Barrier level
            is_call: True for call, False for put
            is_up: True for up barrier, False for down barrier
            is_knock_in: True for knock-in, False for knock-out
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        option_type = 0 if is_call else 1  # FDP_OPTION_CALL = 0, FDP_OPTION_PUT = 1

        # Determine barrier type
        if is_up and is_knock_in:
            barrier_type = 0  # FDP_BARRIER_UP_AND_IN
        elif is_up and not is_knock_in:
            barrier_type = 1  # FDP_BARRIER_UP_AND_OUT
        elif not is_up and is_knock_in:
            barrier_type = 2  # FDP_BARRIER_DOWN_AND_IN
        else:
            barrier_type = 3  # FDP_BARRIER_DOWN_AND_OUT

        result = self._lib.fdp_price_barrier_option(
            spot, strike, rate, div_yield, vol, maturity, barrier,
            option_type, barrier_type, n_space, n_time
        )
        return self._check_result(result, "Barrier option pricing")

    # -------------------------------------------------------------------------
    # Convenience API - Asian Options
    # -------------------------------------------------------------------------

    def price_asian_call(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price an Asian call option (arithmetic average).

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_asian_call(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "Asian call pricing")

    def price_asian_put(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price an Asian put option (arithmetic average).

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_asian_put(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "Asian put pricing")

    # -------------------------------------------------------------------------
    # Convenience API - Digital Options
    # -------------------------------------------------------------------------

    def price_digital_call(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price a digital (binary) call option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_digital_call(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "Digital call pricing")

    def price_digital_put(
        self,
        spot: float,
        strike: float,
        rate: float,
        div_yield: float,
        vol: float,
        maturity: float,
        n_space: int = 200,
        n_time: int = 100,
    ) -> float:
        """Price a digital (binary) put option.

        Args:
            spot: Current spot price
            strike: Strike price
            rate: Risk-free rate (annualized)
            div_yield: Dividend yield (annualized)
            vol: Volatility (annualized)
            maturity: Time to maturity (years)
            n_space: Number of spatial grid points
            n_time: Number of time steps

        Returns:
            Option price
        """
        result = self._lib.fdp_price_digital_put(
            spot, strike, rate, div_yield, vol, maturity, n_space, n_time
        )
        return self._check_result(result, "Digital put pricing")

    # -------------------------------------------------------------------------
    # Full API - Context Management
    # -------------------------------------------------------------------------

    def create_context(self) -> FDPContext:
        """Create a new pricing context.

        Returns:
            FDPContext for use with full API
        """
        return FDPContext(self._ffi, self._lib)


class FDPContext:
    """Context for advanced pricing operations.

    Use this when you need fine-grained control over the pricing
    process, or when pricing many options with similar parameters.
    """

    def __init__(self, ffi: FFI, lib: object) -> None:
        """Initialize context (internal use only)."""
        self._ffi = ffi
        self._lib = lib
        self._ctx = lib.fdp_context_new()
        if self._ctx == ffi.NULL:
            raise FDPricingError("Failed to create context")

    def __del__(self) -> None:
        """Clean up context."""
        if hasattr(self, "_ctx") and self._ctx != self._ffi.NULL:
            self._lib.fdp_context_free(self._ctx)

    def __enter__(self) -> FDPContext:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        if self._ctx != self._ffi.NULL:
            self._lib.fdp_context_free(self._ctx)
            self._ctx = self._ffi.NULL

    def get_error(self) -> str:
        """Get the last error message.

        Returns:
            Error message string
        """
        err = self._lib.fdp_context_get_error(self._ctx)
        return self._ffi.string(self._lib.fdp_error_string(err)).decode()
