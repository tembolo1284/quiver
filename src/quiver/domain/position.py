"""Position domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Self
from uuid import UUID, uuid4

from quiver.domain.option import Option
from quiver.pricing.result import Greeks, PricingResult


@dataclass(slots=True)
class Position:
    """A position in an option contract.

    Tracks quantity held, entry price, and current valuation.

    Attributes:
        option: The option contract
        quantity: Number of contracts (negative for short)
        entry_price: Price paid per contract at entry
        entry_date: Date position was opened
        id: Unique position identifier
        current_price: Current model price (updated on refresh)
        greeks: Current Greeks (updated on refresh)
        spot: Current underlying spot price
        last_updated: Timestamp of last price update
    """

    option: Option
    quantity: int
    entry_price: float
    entry_date: date = field(default_factory=date.today)
    id: UUID = field(default_factory=uuid4)

    # Mutable pricing state
    current_price: float | None = field(default=None, compare=False)
    greeks: Greeks | None = field(default=None, compare=False)
    spot: float | None = field(default=None, compare=False)
    last_updated: datetime | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        """Validate position parameters."""
        if self.quantity == 0:
            raise ValueError("Quantity cannot be zero")
        if self.entry_price < 0:
            raise ValueError(f"Entry price must be non-negative, got {self.entry_price}")

    @property
    def is_long(self) -> bool:
        """Return True if this is a long position."""
        return self.quantity > 0

    @property
    def is_short(self) -> bool:
        """Return True if this is a short position."""
        return self.quantity < 0

    @property
    def notional(self) -> float:
        """Calculate entry notional value (quantity * entry_price * 100)."""
        return abs(self.quantity) * self.entry_price * 100

    @property
    def current_value(self) -> float | None:
        """Calculate current market value."""
        if self.current_price is None:
            return None
        return self.quantity * self.current_price * 100

    @property
    def pnl(self) -> float | None:
        """Calculate unrealized P&L."""
        if self.current_price is None:
            return None
        return self.quantity * (self.current_price - self.entry_price) * 100

    @property
    def pnl_percent(self) -> float | None:
        """Calculate P&L as percentage of entry value."""
        if self.current_price is None or self.entry_price == 0:
            return None
        return (self.current_price - self.entry_price) / self.entry_price * 100

    @property
    def position_delta(self) -> float | None:
        """Calculate position delta (delta * quantity * 100)."""
        if self.greeks is None:
            return None
        return self.greeks.delta * self.quantity * 100

    @property
    def position_gamma(self) -> float | None:
        """Calculate position gamma (gamma * quantity * 100)."""
        if self.greeks is None:
            return None
        return self.greeks.gamma * self.quantity * 100

    @property
    def position_theta(self) -> float | None:
        """Calculate position theta (theta * quantity * 100)."""
        if self.greeks is None:
            return None
        return self.greeks.theta * self.quantity * 100

    @property
    def position_vega(self) -> float | None:
        """Calculate position vega (vega * quantity * 100)."""
        if self.greeks is None:
            return None
        return self.greeks.vega * self.quantity * 100

    def update_pricing(self, result: PricingResult, spot: float) -> None:
        """Update position with new pricing result.

        Args:
            result: New pricing result from engine
            spot: Current spot price of underlying
        """
        self.current_price = result.price
        self.greeks = result.greeks
        self.spot = spot
        self.last_updated = datetime.now()

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        data = {
            "option": self.option.to_dict(),
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "entry_date": self.entry_date.isoformat(),
            "id": str(self.id),
        }
        if self.current_price is not None:
            data["current_price"] = self.current_price
        if self.spot is not None:
            data["spot"] = self.spot
        if self.greeks is not None:
            data["greeks"] = {
                "delta": self.greeks.delta,
                "gamma": self.greeks.gamma,
                "theta": self.greeks.theta,
                "vega": self.greeks.vega,
                "rho": self.greeks.rho,
            }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialize from dictionary."""
        greeks = None
        if "greeks" in data:
            g = data["greeks"]
            greeks = Greeks(
                delta=g["delta"],
                gamma=g["gamma"],
                theta=g["theta"],
                vega=g["vega"],
                rho=g.get("rho", 0.0),
            )

        return cls(
            option=Option.from_dict(data["option"]),
            quantity=data["quantity"],
            entry_price=data["entry_price"],
            entry_date=date.fromisoformat(data["entry_date"]),
            id=UUID(data["id"]),
            current_price=data.get("current_price"),
            spot=data.get("spot"),
            greeks=greeks,
        )
