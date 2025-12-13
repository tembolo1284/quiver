"""Book screen - main positions view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static

from quiver.ui.widgets.greeks_panel import GreeksPanel
from quiver.ui.widgets.positions_table import PositionsTable

if TYPE_CHECKING:
    from quiver.domain.book import Book


class BookScreen(Container):
    """Main book screen showing positions and aggregate Greeks."""

    DEFAULT_CSS = """
    BookScreen {
        layout: grid;
        grid-size: 1;
        grid-rows: 1fr auto;
    }

    #positions-container {
        height: 100%;
    }

    #footer-container {
        height: auto;
        dock: bottom;
    }
    """

    def __init__(self, book: Book) -> None:
        """Initialize the book screen.

        Args:
            book: Book to display
        """
        super().__init__()
        self._book = book

    def compose(self) -> ComposeResult:
        """Compose the screen layout."""
        with Container(id="positions-container"):
            yield PositionsTable(self._book)

        with Horizontal(id="footer-container"):
            yield GreeksPanel(self._book)

    def refresh_all(self) -> None:
        """Refresh all position prices."""
        # Get the table widget and trigger refresh
        table = self.query_one(PositionsTable)
        table.refresh_prices()

    @property
    def book(self) -> Book:
        """Return the book."""
        return self._book
