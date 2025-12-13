"""Quiver TUI application entry point."""
from __future__ import annotations
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header
from quiver.domain.book import Book
from quiver.ui.screens.book_screen import BookScreen

if TYPE_CHECKING:
    pass


class QuiverApp(App[None]):
    """Main Quiver TUI application."""
    TITLE = "Quiver"
    SUB_TITLE = "Options Book"
    CSS_PATH = "ui/styles/app.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh All", show=True),
        Binding("a", "add_position", "Add Position", show=True),
        Binding("d", "delete_position", "Delete", show=True),
        Binding("e", "export", "Export", show=True),
        Binding("?", "help", "Help", show=True),
    ]

    def __init__(
        self,
        book: Book | None = None,
        lib_path: Path | None = None,
    ) -> None:
        """Initialize the application.
        Args:
            book: Optional pre-loaded book. If None, starts with empty book.
            lib_path: Optional path to libfdpricing.so
        """
        super().__init__()
        self.book = book or Book()
        self.lib_path = lib_path
        self._executor = ThreadPoolExecutor(max_workers=4)

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield BookScreen(self.book)
        yield Footer()

    async def on_mount(self) -> None:
        """Handle application mount."""
        self.log.info("Quiver started")

    def action_quit(self) -> None:
        """Quit the application."""
        self._executor.shutdown(wait=False)
        self.exit()

    def action_refresh(self) -> None:
        """Refresh all position prices."""
        book_screen = self.query_one(BookScreen)
        book_screen.refresh_all()

    def action_add_position(self) -> None:
        """Add a new position."""
        from quiver.ui.screens.add_position_screen import AddPositionScreen

        def handle_result(position) -> None:
            if position is not None:
                self.book.add(position)
                book_screen = self.query_one(BookScreen)
                book_screen.refresh_all()
                self.notify(f"Added {position.option.symbol}", severity="information")

        self.push_screen(AddPositionScreen(), handle_result)

    def action_delete_position(self) -> None:
        """Delete the selected position."""
        self.notify("Delete position: Not yet implemented", severity="warning")

    def action_export(self) -> None:
        """Export book to JSON."""
        self.notify("Export: Not yet implemented", severity="warning")

    def action_help(self) -> None:
        """Show help screen."""
        self.notify("Help: Not yet implemented", severity="warning")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="quiver",
        description="Terminal-based options book with finite difference pricing",
    )
    parser.add_argument(
        "--book",
        type=Path,
        help="Path to book JSON file to load",
    )
    parser.add_argument(
        "--lib-path",
        type=Path,
        help="Path to libfdpricing.so",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    book = None
    if args.book:
        if not args.book.exists():
            print(f"Error: Book file not found: {args.book}", file=sys.stderr)
            return 1
        book = Book.load(args.book)
    app = QuiverApp(book=book, lib_path=args.lib_path)
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
