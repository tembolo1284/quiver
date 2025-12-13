"""Add position modal screen."""

from __future__ import annotations

from datetime import date, timedelta

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static

from quiver.domain.option import Option, OptionStyle, OptionType
from quiver.domain.position import Position


class AddPositionScreen(ModalScreen[Position | None]):
    """Modal screen for adding a new position."""

    CSS = """
    AddPositionScreen {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: thick $primary;
    }

    #title {
        text-style: bold;
        color: $primary;
        width: 100%;
        content-align: center middle;
        padding-bottom: 1;
    }

    .field-row {
        height: 3;
        margin-bottom: 1;
    }

    .field-label {
        width: 12;
        height: 3;
        content-align: left middle;
    }

    .field-input {
        width: 1fr;
    }

    #buttons {
        height: 3;
        margin-top: 1;
        align: center middle;
    }

    #buttons Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the dialog layout."""
        with Vertical(id="dialog"):
            yield Static("Add New Position", id="title")

            with Horizontal(classes="field-row"):
                yield Label("Symbol:", classes="field-label")
                yield Input(placeholder="AAPL", id="symbol", classes="field-input")

            with Horizontal(classes="field-row"):
                yield Label("Strike:", classes="field-label")
                yield Input(placeholder="150.00", id="strike", classes="field-input")

            with Horizontal(classes="field-row"):
                yield Label("Expiry:", classes="field-label")
                yield Input(
                    placeholder="YYYY-MM-DD",
                    id="expiry",
                    value=(date.today() + timedelta(days=30)).isoformat(),
                    classes="field-input",
                )

            with Horizontal(classes="field-row"):
                yield Label("Type:", classes="field-label")
                yield Select(
                    [(name, name) for name in ["CALL", "PUT"]],
                    value="CALL",
                    id="option_type",
                    classes="field-input",
                )

            with Horizontal(classes="field-row"):
                yield Label("Style:", classes="field-label")
                yield Select(
                    [(name, name) for name in ["EUROPEAN", "AMERICAN"]],
                    value="EUROPEAN",
                    id="style",
                    classes="field-input",
                )

            with Horizontal(classes="field-row"):
                yield Label("Quantity:", classes="field-label")
                yield Input(placeholder="10", id="quantity", classes="field-input")

            with Horizontal(classes="field-row"):
                yield Label("Entry $:", classes="field-label")
                yield Input(placeholder="5.50", id="entry_price", classes="field-input")

            with Horizontal(id="buttons"):
                yield Button("Add", variant="primary", id="add")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "add":
            self._add_position()

    def _add_position(self) -> None:
        """Validate and create the position."""
        try:
            symbol = self.query_one("#symbol", Input).value.strip().upper()
            strike = float(self.query_one("#strike", Input).value)
            expiry_str = self.query_one("#expiry", Input).value.strip()
            option_type_str = self.query_one("#option_type", Select).value
            style_str = self.query_one("#style", Select).value
            quantity = int(self.query_one("#quantity", Input).value)
            entry_price = float(self.query_one("#entry_price", Input).value)

            if not symbol:
                self.notify("Symbol is required", severity="error")
                return

            expiry = date.fromisoformat(expiry_str)
            option_type = OptionType[option_type_str]
            style = OptionStyle[style_str]

            option = Option(
                underlying=symbol,
                strike=strike,
                expiry=expiry,
                option_type=option_type,
                style=style,
            )

            position = Position(
                option=option,
                quantity=quantity,
                entry_price=entry_price,
            )

            self.dismiss(position)

        except ValueError as e:
            self.notify(f"Invalid input: {e}", severity="error")
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")
