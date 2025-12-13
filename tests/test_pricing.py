"""Tests for pricing layer."""

import pytest

from quiver.pricing.params import GridParams, GridType, ModelParams, ModelType
from quiver.pricing.result import Greeks, PricingResult


class TestGreeks:
    """Tests for Greeks value object."""

    def test_create_greeks(self):
        """Test creating Greeks."""
        greeks = Greeks(
            delta=0.62,
            gamma=0.031,
            theta=-0.089,
            vega=0.45,
            rho=0.21,
        )
        assert greeks.delta == 0.62
        assert greeks.gamma == 0.031
        assert greeks.theta == -0.089
        assert greeks.vega == 0.45
        assert greeks.rho == 0.21

    def test_greeks_immutable(self, sample_greeks: Greeks):
        """Test that Greeks are immutable."""
        with pytest.raises(AttributeError):
            sample_greeks.delta = 0.5  # type: ignore

    def test_greeks_scaled(self, sample_greeks: Greeks):
        """Test scaling Greeks by position size."""
        scaled = sample_greeks.scaled(quantity=10, multiplier=100)
        assert scaled.delta == pytest.approx(sample_greeks.delta * 1000)
        assert scaled.gamma == pytest.approx(sample_greeks.gamma * 1000)


class TestPricingResult:
    """Tests for PricingResult value object."""

    def test_create_result(self, sample_greeks: Greeks):
        """Test creating a pricing result."""
        result = PricingResult(
            price=12.45,
            greeks=sample_greeks,
            model_type="GBM",
            grid_points=200,
            time_steps=100,
        )
        assert result.price == 12.45
        assert result.greeks == sample_greeks
        assert result.model_type == "GBM"

    def test_convenience_accessors(self, sample_greeks: Greeks):
        """Test Greek convenience accessors."""
        result = PricingResult(price=12.45, greeks=sample_greeks)
        assert result.delta == sample_greeks.delta
        assert result.gamma == sample_greeks.gamma
        assert result.theta == sample_greeks.theta
        assert result.vega == sample_greeks.vega


class TestModelParams:
    """Tests for ModelParams."""

    def test_default_params(self):
        """Test default model parameters."""
        params = ModelParams()
        assert params.rate == 0.05
        assert params.div_yield == 0.0
        assert params.vol == 0.20
        assert params.model_type == ModelType.GBM

    def test_custom_params(self):
        """Test custom model parameters."""
        params = ModelParams(
            rate=0.03,
            div_yield=0.01,
            vol=0.25,
            model_type=ModelType.HESTON,
        )
        assert params.rate == 0.03
        assert params.model_type == ModelType.HESTON


class TestGridParams:
    """Tests for GridParams."""

    def test_default_grid_params(self):
        """Test default grid parameters."""
        params = GridParams()
        assert params.n_space == 200
        assert params.n_time == 100
        assert params.grid_type == GridType.SINH

    def test_invalid_n_space_raises(self):
        """Test that invalid n_space raises ValueError."""
        with pytest.raises(ValueError, match="n_space must be >= 10"):
            GridParams(n_space=5)

    def test_invalid_n_time_raises(self):
        """Test that invalid n_time raises ValueError."""
        with pytest.raises(ValueError, match="n_time must be >= 10"):
            GridParams(n_time=5)

    def test_invalid_s_min_mult_raises(self):
        """Test that invalid s_min_mult raises ValueError."""
        with pytest.raises(ValueError, match="s_min_mult must be in"):
            GridParams(s_min_mult=1.5)

    def test_invalid_s_max_mult_raises(self):
        """Test that invalid s_max_mult raises ValueError."""
        with pytest.raises(ValueError, match="s_max_mult must be > 1"):
            GridParams(s_max_mult=0.5)
