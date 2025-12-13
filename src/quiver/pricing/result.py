"""Pricing result value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Greeks:
    """Option Greeks.

    Attributes:
        delta: Rate of change of price with respect to spot
        gamma: Rate of change of delta with respect to spot
        theta: Rate of change of price with respect to time (per day)
        vega: Rate of change of price with respect to volatility
        rho: Rate of change of price with respect to interest rate
    """

    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float = 0.0

    def scaled(self, quantity: int, multiplier: int = 100) -> Greeks:
        """Return Greeks scaled by position size.

        Args:
            quantity: Number of contracts
            multiplier: Contract multiplier (default 100)

        Returns:
            Scaled Greeks
        """
        scale = quantity * multiplier
        return Greeks(
            delta=self.delta * scale,
            gamma=self.gamma * scale,
            theta=self.theta * scale,
            vega=self.vega * scale,
            rho=self.rho * scale,
        )


@dataclass(frozen=True, slots=True)
class PricingResult:
    """Result from pricing an option.

    Attributes:
        price: Option price
        greeks: Option Greeks
        model_type: Model used for pricing (e.g., "GBM", "Heston")
        grid_points: Number of spatial grid points used
        time_steps: Number of time steps used
    """

    price: float
    greeks: Greeks
    model_type: str = "GBM"
    grid_points: int = 200
    time_steps: int = 100

    @property
    def delta(self) -> float:
        """Convenience accessor for delta."""
        return self.greeks.delta

    @property
    def gamma(self) -> float:
        """Convenience accessor for gamma."""
        return self.greeks.gamma

    @property
    def theta(self) -> float:
        """Convenience accessor for theta."""
        return self.greeks.theta

    @property
    def vega(self) -> float:
        """Convenience accessor for vega."""
        return self.greeks.vega

    @property
    def rho(self) -> float:
        """Convenience accessor for rho."""
        return self.greeks.rho
