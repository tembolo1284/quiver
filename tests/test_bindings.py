"""Tests for CFFI bindings.

These tests require libfdpricing.so to be available.
Tests are skipped if the library is not found.
"""

import pytest

# Try to import bindings, skip all tests if library not found
try:
    from quiver.bindings.fdpricing import FDPricing, FDPricingNotFoundError

    _fdp = FDPricing()
    LIBRARY_AVAILABLE = True
except (ImportError, FDPricingNotFoundError):
    LIBRARY_AVAILABLE = False
    FDPricing = None  # type: ignore


pytestmark = pytest.mark.skipif(
    not LIBRARY_AVAILABLE,
    reason="libfdpricing.so not available",
)


@pytest.fixture
def fdp() -> FDPricing:
    """Get FDPricing instance."""
    return FDPricing()


class TestEuropeanOptions:
    """Tests for European option pricing."""

    def test_european_call_atm(self, fdp: FDPricing):
        """Test pricing ATM European call."""
        price = fdp.price_european_call(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
            n_space=200,
            n_time=100,
        )
        # Should be close to Black-Scholes analytical: ~10.45
        assert 9.0 < price < 12.0

    def test_european_put_atm(self, fdp: FDPricing):
        """Test pricing ATM European put."""
        price = fdp.price_european_put(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
            n_space=200,
            n_time=100,
        )
        # Put-call parity check
        assert 4.0 < price < 8.0

    def test_european_call_itm(self, fdp: FDPricing):
        """Test pricing ITM European call."""
        price = fdp.price_european_call(
            spot=120.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        # ITM call should have significant intrinsic value
        assert price > 20.0

    def test_european_call_otm(self, fdp: FDPricing):
        """Test pricing OTM European call."""
        price = fdp.price_european_call(
            spot=80.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        # OTM call should be small but positive
        assert 0.0 < price < 5.0


class TestAmericanOptions:
    """Tests for American option pricing."""

    def test_american_put_atm(self, fdp: FDPricing):
        """Test pricing ATM American put."""
        price = fdp.price_american_put(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        # American put should be worth at least as much as European
        assert price > 5.0

    def test_american_call_no_dividend(self, fdp: FDPricing):
        """Test that American call equals European when no dividends."""
        amer_price = fdp.price_american_call(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        euro_price = fdp.price_european_call(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        # Should be very close when no dividends
        assert abs(amer_price - euro_price) < 0.5

    def test_american_put_early_exercise_premium(self, fdp: FDPricing):
        """Test that American put has early exercise premium."""
        amer_price = fdp.price_american_put(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        euro_price = fdp.price_european_put(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            div_yield=0.0,
            vol=0.20,
            maturity=1.0,
        )
        # American put should be worth more
        assert amer_price >= euro_price


class TestPutCallParity:
    """Tests for put-call parity relationships."""

    def test_put_call_parity_european(self, fdp: FDPricing):
        """Test put-call parity for European options."""
        import math

        spot = 100.0
        strike = 100.0
        rate = 0.05
        div_yield = 0.02
        vol = 0.20
        maturity = 1.0

        call = fdp.price_european_call(
            spot, strike, rate, div_yield, vol, maturity
        )
        put = fdp.price_european_put(
            spot, strike, rate, div_yield, vol, maturity
        )

        # C - P = S*exp(-q*T) - K*exp(-r*T)
        forward_diff = spot * math.exp(-div_yield * maturity) - strike * math.exp(
            -rate * maturity
        )
        parity_diff = call - put

        # Should hold within numerical tolerance
        assert abs(parity_diff - forward_diff) < 0.5


@pytest.mark.integration
class TestPricingEngine:
    """Integration tests for FDPricingEngine."""

    def test_engine_prices_european_call(self):
        """Test engine prices European call option."""
        from datetime import date, timedelta

        from quiver.domain.option import Option, OptionStyle, OptionType
        from quiver.pricing.engine import FDPricingEngine
        from quiver.pricing.params import ModelParams

        engine = FDPricingEngine()
        option = Option(
            underlying="TEST",
            strike=100.0,
            expiry=date.today() + timedelta(days=365),
            option_type=OptionType.CALL,
            style=OptionStyle.EUROPEAN,
        )
        params = ModelParams(rate=0.05, div_yield=0.0, vol=0.20)

        result = engine.price(option, spot=100.0, params=params)

        assert result.price > 0
        assert -1 <= result.delta <= 1
        assert result.gamma >= 0
