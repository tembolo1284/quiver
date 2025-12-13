"""Pytest fixtures for quiver tests."""

from datetime import date, timedelta

import pytest

from quiver.domain.book import Book
from quiver.domain.option import Option, OptionStyle, OptionType
from quiver.domain.position import Position
from quiver.pricing.result import Greeks


@pytest.fixture
def sample_option() -> Option:
    """Create a sample European call option."""
    return Option(
        underlying="AAPL",
        strike=180.0,
        expiry=date.today() + timedelta(days=30),
        option_type=OptionType.CALL,
        style=OptionStyle.EUROPEAN,
    )


@pytest.fixture
def sample_put_option() -> Option:
    """Create a sample European put option."""
    return Option(
        underlying="SPY",
        strike=450.0,
        expiry=date.today() + timedelta(days=60),
        option_type=OptionType.PUT,
        style=OptionStyle.EUROPEAN,
    )


@pytest.fixture
def sample_american_option() -> Option:
    """Create a sample American put option."""
    return Option(
        underlying="NVDA",
        strike=900.0,
        expiry=date.today() + timedelta(days=45),
        option_type=OptionType.PUT,
        style=OptionStyle.AMERICAN,
    )


@pytest.fixture
def sample_position(sample_option: Option) -> Position:
    """Create a sample position."""
    return Position(
        option=sample_option,
        quantity=10,
        entry_price=12.50,
        entry_date=date.today() - timedelta(days=5),
    )


@pytest.fixture
def sample_short_position(sample_put_option: Option) -> Position:
    """Create a sample short position."""
    return Position(
        option=sample_put_option,
        quantity=-5,
        entry_price=8.20,
        entry_date=date.today() - timedelta(days=10),
    )


@pytest.fixture
def sample_greeks() -> Greeks:
    """Create sample Greeks."""
    return Greeks(
        delta=0.62,
        gamma=0.031,
        theta=-0.089,
        vega=0.45,
        rho=0.21,
    )


@pytest.fixture
def position_with_pricing(sample_position: Position, sample_greeks: Greeks) -> Position:
    """Create a position with pricing data."""
    from quiver.pricing.result import PricingResult

    result = PricingResult(price=14.75, greeks=sample_greeks)
    sample_position.update_pricing(result, spot=185.50)
    return sample_position


@pytest.fixture
def sample_book(sample_position: Position, sample_short_position: Position) -> Book:
    """Create a sample book with positions."""
    book = Book(name="Test Book")
    book.add(sample_position)
    book.add(sample_short_position)
    return book


@pytest.fixture
def empty_book() -> Book:
    """Create an empty book."""
    return Book(name="Empty Book")
