"""Tests for domain layer."""

from datetime import date, timedelta
from uuid import UUID

import pytest

from quiver.domain.book import Book
from quiver.domain.option import Option, OptionStyle, OptionType
from quiver.domain.position import Position
from quiver.pricing.result import Greeks, PricingResult


class TestOption:
    """Tests for Option entity."""

    def test_create_call_option(self):
        """Test creating a call option."""
        opt = Option(
            underlying="AAPL",
            strike=180.0,
            expiry=date(2024, 6, 21),
            option_type=OptionType.CALL,
            style=OptionStyle.EUROPEAN,
        )
        assert opt.underlying == "AAPL"
        assert opt.strike == 180.0
        assert opt.is_call
        assert not opt.is_put
        assert not opt.is_barrier

    def test_create_put_option(self):
        """Test creating a put option."""
        opt = Option(
            underlying="SPY",
            strike=450.0,
            expiry=date(2024, 7, 19),
            option_type=OptionType.PUT,
            style=OptionStyle.AMERICAN,
        )
        assert opt.is_put
        assert not opt.is_call
        assert opt.style == OptionStyle.AMERICAN

    def test_invalid_strike_raises(self):
        """Test that invalid strike raises ValueError."""
        with pytest.raises(ValueError, match="Strike must be positive"):
            Option(
                underlying="AAPL",
                strike=-100.0,
                expiry=date(2024, 6, 21),
                option_type=OptionType.CALL,
            )

    def test_time_to_expiry(self):
        """Test time to expiry calculation."""
        expiry = date.today() + timedelta(days=365)
        opt = Option(
            underlying="AAPL",
            strike=180.0,
            expiry=expiry,
            option_type=OptionType.CALL,
        )
        tte = opt.time_to_expiry()
        assert 0.99 < tte < 1.01  # Approximately 1 year

    def test_expired_option_tte_is_zero(self):
        """Test that expired options have zero time to expiry."""
        opt = Option(
            underlying="AAPL",
            strike=180.0,
            expiry=date.today() - timedelta(days=1),
            option_type=OptionType.CALL,
        )
        assert opt.time_to_expiry() == 0.0

    def test_symbol_generation(self):
        """Test option symbol generation."""
        opt = Option(
            underlying="AAPL",
            strike=180.0,
            expiry=date(2024, 6, 21),
            option_type=OptionType.CALL,
        )
        assert "AAPL" in opt.symbol
        assert "180" in opt.symbol
        assert "C" in opt.symbol

    def test_serialization_roundtrip(self, sample_option: Option):
        """Test option serialization and deserialization."""
        data = sample_option.to_dict()
        restored = Option.from_dict(data)
        assert restored == sample_option


class TestPosition:
    """Tests for Position entity."""

    def test_create_long_position(self, sample_option: Option):
        """Test creating a long position."""
        pos = Position(
            option=sample_option,
            quantity=10,
            entry_price=12.50,
        )
        assert pos.is_long
        assert not pos.is_short
        assert pos.quantity == 10
        assert pos.entry_price == 12.50
        assert isinstance(pos.id, UUID)

    def test_create_short_position(self, sample_option: Option):
        """Test creating a short position."""
        pos = Position(
            option=sample_option,
            quantity=-5,
            entry_price=12.50,
        )
        assert pos.is_short
        assert not pos.is_long

    def test_zero_quantity_raises(self, sample_option: Option):
        """Test that zero quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity cannot be zero"):
            Position(option=sample_option, quantity=0, entry_price=10.0)

    def test_negative_entry_price_raises(self, sample_option: Option):
        """Test that negative entry price raises ValueError."""
        with pytest.raises(ValueError, match="Entry price must be non-negative"):
            Position(option=sample_option, quantity=10, entry_price=-5.0)

    def test_notional_calculation(self, sample_position: Position):
        """Test notional value calculation."""
        # quantity=10, entry_price=12.50, multiplier=100
        expected = 10 * 12.50 * 100
        assert sample_position.notional == expected

    def test_pnl_before_pricing(self, sample_position: Position):
        """Test that P&L is None before pricing."""
        assert sample_position.pnl is None
        assert sample_position.current_value is None

    def test_pnl_after_pricing(self, position_with_pricing: Position):
        """Test P&L calculation after pricing update."""
        pos = position_with_pricing
        # entry_price=12.50, current_price=14.75, quantity=10
        expected_pnl = 10 * (14.75 - 12.50) * 100
        assert pos.pnl == pytest.approx(expected_pnl)

    def test_position_greeks(self, position_with_pricing: Position):
        """Test position Greeks scaling."""
        pos = position_with_pricing
        # delta=0.62, quantity=10, multiplier=100
        expected_delta = 0.62 * 10 * 100
        assert pos.position_delta == pytest.approx(expected_delta)

    def test_serialization_roundtrip(self, sample_position: Position):
        """Test position serialization and deserialization."""
        data = sample_position.to_dict()
        restored = Position.from_dict(data)
        assert restored.option == sample_position.option
        assert restored.quantity == sample_position.quantity
        assert restored.entry_price == sample_position.entry_price


class TestBook:
    """Tests for Book aggregate."""

    def test_empty_book(self, empty_book: Book):
        """Test empty book properties."""
        assert len(empty_book) == 0
        assert empty_book.total_pnl is None
        assert empty_book.total_greeks is None

    def test_add_position(self, empty_book: Book, sample_position: Position):
        """Test adding a position to a book."""
        empty_book.add(sample_position)
        assert len(empty_book) == 1
        assert empty_book.positions[0] == sample_position

    def test_remove_position(self, sample_book: Book):
        """Test removing a position from a book."""
        initial_count = len(sample_book)
        pos_id = sample_book.positions[0].id

        removed = sample_book.remove(pos_id)

        assert removed is not None
        assert len(sample_book) == initial_count - 1

    def test_get_position(self, sample_book: Book):
        """Test getting a position by ID."""
        pos_id = sample_book.positions[0].id
        found = sample_book.get(pos_id)
        assert found is not None
        assert found.id == pos_id

    def test_get_nonexistent_position(self, sample_book: Book):
        """Test getting a nonexistent position returns None."""
        from uuid import uuid4

        found = sample_book.get(uuid4())
        assert found is None

    def test_underlyings(self, sample_book: Book):
        """Test getting unique underlyings."""
        underlyings = sample_book.underlyings
        assert "AAPL" in underlyings
        assert "SPY" in underlyings

    def test_get_by_underlying(self, sample_book: Book):
        """Test filtering positions by underlying."""
        aapl_positions = sample_book.get_by_underlying("AAPL")
        assert len(aapl_positions) == 1
        assert aapl_positions[0].option.underlying == "AAPL"

    def test_iteration(self, sample_book: Book):
        """Test iterating over book positions."""
        positions = list(sample_book)
        assert len(positions) == 2

    def test_indexing(self, sample_book: Book):
        """Test indexing book positions."""
        first = sample_book[0]
        assert first == sample_book.positions[0]

    def test_serialization_roundtrip(self, sample_book: Book, tmp_path):
        """Test book save and load."""
        path = tmp_path / "test_book.json"
        sample_book.save(path)

        loaded = Book.load(path)

        assert loaded.name == sample_book.name
        assert len(loaded) == len(sample_book)
