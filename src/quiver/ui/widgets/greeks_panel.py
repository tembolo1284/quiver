"""Greeks panel widget for aggregate Greeks display."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import Static

if TYPE_CHECKING:
    from quiver.domain.book import Book


class GreeksPanel(Static):
    """Panel showing aggregate Greeks for the entire book."""

    DEFAULT_CSS = """
    GreeksPanel {
        height: 3;
        padding: 0 2;
        background: $surface;
        border-top: solid $primary;
    }
    """

    def __init__(self, book: Book) -> None:
        """Initialize the Greeks panel.

        Args:
            book: Book to aggregate Greeks from
        """
        super().__init__()
        self._book = book

    def on_mount(self) -> None:
        """Update display when mounted."""
        self._update_display()

    def _update_display(self) -> None:
        """Update the displayed Greeks."""
        greeks = self._book.total_greeks
        pnl = self._book.total_pnl

        if greeks is not None:
            delta_str = f"Δ {greeks.delta:+,.0f}"
            gamma_str = f"Γ {greeks.gamma:+,.0f}"
            theta_str = f"Θ {greeks.theta:+,.0f}"
            vega_str = f"V {greeks.vega:+,.0f}"
        else:
            delta_str = "Δ —"
            gamma_str = "Γ —"
            theta_str = "Θ —"
            vega_str = "V —"

        if pnl is not None:
            if pnl >= 0:
                pnl_str = f"[green]P&L: +${pnl:,.0f}[/green]"
            else:
                pnl_str = f"[red]P&L: -${abs(pnl):,.0f}[/red]"
        else:
            pnl_str = "P&L: —"

        # Format as single line with spacing
        content = f"Book Greeks:  {delta_str}   {gamma_str}   {theta_str}   {vega_str}        {pnl_str}"
        self.update(content)

    def refresh_greeks(self) -> None:
        """Refresh the displayed Greeks."""
        self._update_display()
