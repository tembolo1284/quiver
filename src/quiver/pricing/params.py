"""Pricing parameters."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ModelType(Enum):
    """Pricing model type."""

    GBM = auto()  # Geometric Brownian Motion (Black-Scholes)
    HESTON = auto()  # Heston stochastic volatility
    SABR = auto()  # SABR model
    MERTON = auto()  # Merton jump-diffusion


class GridType(Enum):
    """Grid type for finite difference solver."""

    UNIFORM = auto()
    SINH = auto()  # Sinh-concentrated around strike
    LOG = auto()  # Logarithmic spacing


@dataclass(frozen=True, slots=True)
class ModelParams:
    """Parameters for the pricing model.

    Attributes:
        rate: Risk-free interest rate (annualized)
        div_yield: Dividend yield (annualized)
        vol: Volatility (annualized)
        model_type: Type of model to use

        # Heston parameters (if model_type == HESTON)
        heston_v0: Initial variance
        heston_kappa: Mean reversion speed
        heston_theta: Long-term variance
        heston_sigma: Vol of vol
        heston_rho: Correlation

        # SABR parameters (if model_type == SABR)
        sabr_alpha: Initial vol
        sabr_beta: CEV exponent
        sabr_rho: Correlation
        sabr_nu: Vol of vol

        # Merton parameters (if model_type == MERTON)
        merton_lambda: Jump intensity
        merton_mu_j: Jump mean
        merton_sigma_j: Jump volatility
    """

    rate: float = 0.05
    div_yield: float = 0.0
    vol: float = 0.20
    model_type: ModelType = ModelType.GBM

    # Heston parameters
    heston_v0: float = 0.04
    heston_kappa: float = 2.0
    heston_theta: float = 0.04
    heston_sigma: float = 0.3
    heston_rho: float = -0.7

    # SABR parameters
    sabr_alpha: float = 0.2
    sabr_beta: float = 0.5
    sabr_rho: float = -0.3
    sabr_nu: float = 0.4

    # Merton parameters
    merton_lambda: float = 0.1
    merton_mu_j: float = -0.1
    merton_sigma_j: float = 0.2


@dataclass(frozen=True, slots=True)
class GridParams:
    """Parameters for the finite difference grid.

    Attributes:
        n_space: Number of spatial grid points
        n_time: Number of time steps
        grid_type: Type of grid spacing
        s_min_mult: Minimum spot as multiple of strike (e.g., 0.2 = 20% of strike)
        s_max_mult: Maximum spot as multiple of strike (e.g., 3.0 = 300% of strike)
    """

    n_space: int = 200
    n_time: int = 100
    grid_type: GridType = GridType.SINH
    s_min_mult: float = 0.2
    s_max_mult: float = 3.0

    def __post_init__(self) -> None:
        """Validate grid parameters."""
        if self.n_space < 10:
            raise ValueError(f"n_space must be >= 10, got {self.n_space}")
        if self.n_time < 10:
            raise ValueError(f"n_time must be >= 10, got {self.n_time}")
        if self.s_min_mult <= 0 or self.s_min_mult >= 1:
            raise ValueError(f"s_min_mult must be in (0, 1), got {self.s_min_mult}")
        if self.s_max_mult <= 1:
            raise ValueError(f"s_max_mult must be > 1, got {self.s_max_mult}")
