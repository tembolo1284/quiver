"""Positions table widget."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text
from textual.widgets import DataTable

if TYPE_CHECKING:
    from quiver.domain.book import Book
    from quiver.domain.position import Position


class PositionsTable(DataTable):
    """DataTable widget displaying positions in the book."""

    DEFAULT_CSS = """
    PositionsTable {
        height: 100%;
    }
    """

    COLUMNS = [
        ("Symbol", 16),
        ("Strike", 10),
        ("Expiry", 12),
        ("Qty", 8),
        ("Price", 10),
        ("Delta", 10),
        ("Gamma", 10),
        ("P&L", 12),
    ]

    def __init__(self, book: Book) -> None:
        """Initialize the positions table.

        Args:
            book: Book containing positions to display
        """
        super().__init__()
        self._book = book
        self.cursor_type = "row"
        self.zebra_stripes = True

    def on_mount(self) -> None:
        """Set up the table when mounted."""
        # Add columns
        for name, width in self.COLUMNS:
            self.add_column(name, width=width)

        # Add initial rows
        self._refresh_rows()

    def _refresh_rows(self) -> None:
        """Refresh all rows from the book."""
        self.clear()

        for position in self._book:
            self.add_row(*self._format_position(position), key=str(position.id))

    def _format_position(self, pos: Position) -> tuple:
        """Format a position for display.

        Args:
            pos: Position to format

        Returns:
            Tuple of formatted cell values
        """
        # Symbol
        symbol = pos.option.symbol

        # Strike
        strike = f"${pos.option.strike:,.2f}"

        # Expiry
        expiry = pos.option.expiry.strftime("%Y-%m-%d")

        # Quantity (with sign)
        qty = f"{pos.quantity:+d}"

        # Price
        if pos.current_price is not None:
            price = f"${pos.current_price:,.4f}"
        else:
            price = "—"

        # Delta
        if pos.greeks is not None:
            delta = f"{pos.greeks.delta:+.4f}"
        else:
            delta = "—"

        # Gamma
        if pos.greeks is not None:
            gamma = f"{pos.greeks.gamma:.5f}"
        else:
            gamma = "—"

        # P&L
        if pos.pnl is not None:
            pnl_val = pos.pnl
            if pnl_val >= 0:
                pnl = Text(f"+${pnl_val:,.0f}", style="green")
            else:
                pnl = Text(f"-${abs(pnl_val):,.0f}", style="red")
        else:
            pnl = "—"

        return (symbol, strike, expiry, qty, price, delta, gamma, pnl)

    def refresh_table(self) -> None:
        """Refresh the table display."""
        self._refresh_rows()

    def refresh_prices(self) -> None:
        """Trigger a price refresh (called from old code path)."""
        self.refresh_table()

    @property
    def selected_position_id(self) -> str | None:
        """Return the ID of the currently selected position."""
        if self.cursor_row is not None:
            row_key = self.get_row_at(self.cursor_row)
            if row_key:
                return str(row_key.key)
        return None
