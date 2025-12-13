"""Option domain entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum, auto
from typing import Self


class OptionType(Enum):
    """Option type - call or put."""

    CALL = auto()
    PUT = auto()

    def __str__(self) -> str:
        return "C" if self == OptionType.CALL else "P"


class OptionStyle(Enum):
    """Option exercise style."""

    EUROPEAN = auto()
    AMERICAN = auto()
    BERMUDAN = auto()

    def __str__(self) -> str:
        return self.name.capitalize()


class BarrierType(Enum):
    """Barrier option type."""

    UP_AND_IN = auto()
    UP_AND_OUT = auto()
    DOWN_AND_IN = auto()
    DOWN_AND_OUT = auto()


@dataclass(frozen=True, slots=True)
class Option:
    """Immutable option contract specification.

    Attributes:
        underlying: Underlying asset symbol (e.g., "AAPL", "SPY")
        strike: Strike price
        expiry: Expiration date
        option_type: Call or Put
        style: Exercise style (European, American, etc.)
        barrier: Optional barrier level for barrier options
        barrier_type: Type of barrier (if barrier is set)
    """

    underlying: str
    strike: float
    expiry: date
    option_type: OptionType
    style: OptionStyle = OptionStyle.EUROPEAN
    barrier: float | None = None
    barrier_type: BarrierType | None = None

    def __post_init__(self) -> None:
        """Validate option parameters."""
        if self.strike <= 0:
            raise ValueError(f"Strike must be positive, got {self.strike}")
        if self.barrier is not None and self.barrier_type is None:
            raise ValueError("barrier_type required when barrier is set")

    @property
    def symbol(self) -> str:
        """Generate option symbol (simplified format)."""
        type_char = "C" if self.option_type == OptionType.CALL else "P"
        return f"{self.underlying} {self.strike:.0f}{type_char} {self.expiry:%b%y}"

    @property
    def is_call(self) -> bool:
        """Return True if this is a call option."""
        return self.option_type == OptionType.CALL

    @property
    def is_put(self) -> bool:
        """Return True if this is a put option."""
        return self.option_type == OptionType.PUT

    @property
    def is_barrier(self) -> bool:
        """Return True if this is a barrier option."""
        return self.barrier is not None

    def time_to_expiry(self, as_of: date | None = None) -> float:
        """Calculate time to expiry in years.

        Args:
            as_of: Reference date (defaults to today)

        Returns:
            Time to expiry in years (using 365-day convention)
        """
        ref_date = as_of or date.today()
        days = (self.expiry - ref_date).days
        return max(0.0, days / 365.0)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        data = {
            "underlying": self.underlying,
            "strike": self.strike,
            "expiry": self.expiry.isoformat(),
            "option_type": self.option_type.name,
            "style": self.style.name,
        }
        if self.barrier is not None:
            data["barrier"] = self.barrier
            data["barrier_type"] = self.barrier_type.name if self.barrier_type else None
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialize from dictionary."""
        barrier_type = None
        if data.get("barrier_type"):
            barrier_type = BarrierType[data["barrier_type"]]

        return cls(
            underlying=data["underlying"],
            strike=data["strike"],
            expiry=date.fromisoformat(data["expiry"]),
            option_type=OptionType[data["option_type"]],
            style=OptionStyle[data["style"]],
            barrier=data.get("barrier"),
            barrier_type=barrier_type,
        )
