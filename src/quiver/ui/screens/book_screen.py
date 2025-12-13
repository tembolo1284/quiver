"""Book screen - main positions view."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
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
        self._engine = None
        self._executor = ThreadPoolExecutor(max_workers=4)

    def compose(self) -> ComposeResult:
        """Compose the screen layout."""
        with Container(id="positions-container"):
            yield PositionsTable(self._book)

        with Horizontal(id="footer-container"):
            yield GreeksPanel(self._book)

    def _get_engine(self):
        """Lazy-load the pricing engine."""
        if self._engine is None:
            try:
                from quiver.pricing.engine import FDPricingEngine
                self._engine = FDPricingEngine()
                self.app.notify("Pricing engine loaded", severity="information")
            except Exception as e:
                self.app.notify(f"Pricing engine error: {e}", severity="error")
                return None
        return self._engine

    def refresh_all(self) -> None:
        """Refresh all position prices."""
        engine = self._get_engine()
        
        if engine is None:
            # No engine, just refresh display
            table = self.query_one(PositionsTable)
            table.refresh_table()
            return

        from quiver.pricing.params import ModelParams

        self.app.notify("Pricing positions...", severity="information")
        
        # Price each position
        params = ModelParams()  # Use defaults for now
        priced_count = 0
        
        for position in self._book:
            try:
                # For now, use a dummy spot price (in real app, fetch from market data)
                # Using strike as rough proxy for spot
                spot = position.option.strike * 1.02  # Assume slightly ITM
                
                result = engine.price(position.option, spot, params)
                position.update_pricing(result, spot)
                priced_count += 1
            except Exception as e:
                self.app.log.error(f"Error pricing {position.option.symbol}: {e}")

        # Refresh the table and greeks panel
        table = self.query_one(PositionsTable)
        table.refresh_table()
        
        greeks_panel = self.query_one(GreeksPanel)
        greeks_panel.refresh_greeks()

        self.app.notify(f"Priced {priced_count} positions", severity="information")

    @property
    def book(self) -> Book:
        """Return the book."""
        return self._book
