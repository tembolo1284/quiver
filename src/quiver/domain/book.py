"""Book domain aggregate - collection of positions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Self
from uuid import UUID

from quiver.domain.position import Position
from quiver.pricing.result import Greeks


@dataclass(slots=True)
class Book:
    """Aggregate root for managing a collection of positions.

    The Book is the primary entry point for position management,
    providing methods to add, remove, and query positions, as well
    as calculate aggregate Greeks and P&L.

    Attributes:
        name: Optional book name
        positions: List of positions in the book
    """

    name: str = "Default"
    _positions: list[Position] = field(default_factory=list)

    @property
    def positions(self) -> list[Position]:
        """Return list of all positions."""
        return list(self._positions)

    def __len__(self) -> int:
        """Return number of positions in book."""
        return len(self._positions)

    def __iter__(self) -> Iterator[Position]:
        """Iterate over positions."""
        return iter(self._positions)

    def __getitem__(self, index: int) -> Position:
        """Get position by index."""
        return self._positions[index]

    def add(self, position: Position) -> None:
        """Add a position to the book.

        Args:
            position: Position to add
        """
        self._positions.append(position)

    def remove(self, position_id: UUID) -> Position | None:
        """Remove a position by ID.

        Args:
            position_id: UUID of position to remove

        Returns:
            The removed position, or None if not found
        """
        for i, pos in enumerate(self._positions):
            if pos.id == position_id:
                return self._positions.pop(i)
        return None

    def get(self, position_id: UUID) -> Position | None:
        """Get a position by ID.

        Args:
            position_id: UUID of position to find

        Returns:
            The position, or None if not found
        """
        for pos in self._positions:
            if pos.id == position_id:
                return pos
        return None

    def get_by_underlying(self, underlying: str) -> list[Position]:
        """Get all positions for a given underlying.

        Args:
            underlying: Underlying symbol

        Returns:
            List of positions for that underlying
        """
        return [p for p in self._positions if p.option.underlying == underlying]

    @property
    def underlyings(self) -> set[str]:
        """Return set of unique underlying symbols in book."""
        return {p.option.underlying for p in self._positions}

    @property
    def total_pnl(self) -> float | None:
        """Calculate total P&L across all positions."""
        total = 0.0
        for pos in self._positions:
            if pos.pnl is None:
                return None
            total += pos.pnl
        return total

    @property
    def total_greeks(self) -> Greeks | None:
        """Calculate aggregate Greeks across all positions."""
        total_delta = 0.0
        total_gamma = 0.0
        total_theta = 0.0
        total_vega = 0.0
        total_rho = 0.0

        for pos in self._positions:
            if pos.greeks is None:
                return None
            total_delta += pos.position_delta or 0.0
            total_gamma += pos.position_gamma or 0.0
            total_theta += pos.position_theta or 0.0
            total_vega += pos.position_vega or 0.0
            if pos.greeks.rho is not None:
                total_rho += pos.greeks.rho * pos.quantity * 100

        return Greeks(
            delta=total_delta,
            gamma=total_gamma,
            theta=total_theta,
            vega=total_vega,
            rho=total_rho,
        )

    @property
    def total_notional(self) -> float:
        """Calculate total notional value of all positions."""
        return sum(pos.notional for pos in self._positions)

    @property
    def total_current_value(self) -> float | None:
        """Calculate total current market value."""
        total = 0.0
        for pos in self._positions:
            if pos.current_value is None:
                return None
            total += pos.current_value
        return total

    def to_dict(self) -> dict:
        """Serialize book to dictionary."""
        return {
            "name": self.name,
            "positions": [pos.to_dict() for pos in self._positions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialize book from dictionary."""
        book = cls(name=data.get("name", "Default"))
        for pos_data in data.get("positions", []):
            book.add(Position.from_dict(pos_data))
        return book

    def save(self, path: Path) -> None:
        """Save book to JSON file.

        Args:
            path: Path to save to
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> Self:
        """Load book from JSON file.

        Args:
            path: Path to load from

        Returns:
            Loaded book
        """
        with open(path) as f:
            data = json.load(f)
        return cls.from_dict(data)
