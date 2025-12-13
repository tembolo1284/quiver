"""Pricing engine protocol and implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Sequence

from quiver.pricing.params import GridParams, ModelParams, ModelType
from quiver.pricing.result import Greeks, PricingResult

if TYPE_CHECKING:
    from quiver.domain.option import Option


class PricingEngine(Protocol):
    """Protocol for option pricing engines.

    Implementations must provide price() and optionally price_batch()
    for efficient bulk pricing.
    """

    def price(
        self,
        option: Option,
        spot: float,
        params: ModelParams,
        grid_params: GridParams | None = None,
    ) -> PricingResult:
        """Price a single option.

        Args:
            option: Option to price
            spot: Current spot price of underlying
            params: Model parameters
            grid_params: Optional grid parameters (uses defaults if not provided)

        Returns:
            PricingResult with price and Greeks
        """
        ...

    def price_batch(
        self,
        options: Sequence[Option],
        spots: Sequence[float],
        params: Sequence[ModelParams],
        grid_params: GridParams | None = None,
    ) -> list[PricingResult]:
        """Price multiple options.

        Default implementation calls price() in a loop.
        Implementations may override for efficiency.

        Args:
            options: Options to price
            spots: Spot prices for each option
            params: Model parameters for each option
            grid_params: Optional grid parameters (uses defaults if not provided)

        Returns:
            List of PricingResult for each option
        """
        ...


class FDPricingEngine:
    """Finite difference pricing engine using libfdpricing.

    This engine uses CFFI bindings to call the fdpricing C library
    for high-performance option pricing via finite difference methods.
    """

    def __init__(
        self,
        lib_path: str | None = None,
        default_grid_params: GridParams | None = None,
    ) -> None:
        """Initialize the FD pricing engine.

        Args:
            lib_path: Optional path to libfdpricing.so
            default_grid_params: Default grid parameters to use
        """
        self._lib_path = lib_path
        self._default_grid_params = default_grid_params or GridParams()
        self._fdp: FDPricing | None = None

    def _ensure_loaded(self) -> FDPricing:
        """Ensure the CFFI library is loaded."""
        if self._fdp is None:
            from quiver.bindings.fdpricing import FDPricing

            self._fdp = FDPricing(lib_path=self._lib_path)
        return self._fdp

    def price(
        self,
        option: Option,
        spot: float,
        params: ModelParams,
        grid_params: GridParams | None = None,
    ) -> PricingResult:
        """Price a single option using finite differences.

        Args:
            option: Option to price
            spot: Current spot price of underlying
            params: Model parameters
            grid_params: Optional grid parameters

        Returns:
            PricingResult with price and Greeks
        """
        fdp = self._ensure_loaded()
        gp = grid_params or self._default_grid_params

        # Calculate time to expiry
        T = option.time_to_expiry()
        if T <= 0:
            # Expired option
            intrinsic = max(0, spot - option.strike) if option.is_call else max(0, option.strike - spot)
            return PricingResult(
                price=intrinsic,
                greeks=Greeks(delta=1.0 if option.is_call and spot > option.strike else 0.0,
                             gamma=0.0, theta=0.0, vega=0.0, rho=0.0),
                model_type=params.model_type.name,
                grid_points=gp.n_space,
                time_steps=gp.n_time,
            )

        # Use the appropriate pricing function based on model and option type
        if params.model_type == ModelType.GBM:
            result = self._price_gbm(fdp, option, spot, T, params, gp)
        else:
            # For now, fall back to GBM for other models
            # TODO: Implement Heston, SABR, Merton
            result = self._price_gbm(fdp, option, spot, T, params, gp)

        return result

    def _price_gbm(
        self,
        fdp: FDPricing,
        option: Option,
        spot: float,
        T: float,
        params: ModelParams,
        gp: GridParams,
    ) -> PricingResult:
        """Price using GBM model."""
        from quiver.domain.option import OptionStyle, OptionType

        # Select pricing function based on option style
        if option.style == OptionStyle.EUROPEAN:
            if option.option_type == OptionType.CALL:
                price = fdp.price_european_call(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )
            else:
                price = fdp.price_european_put(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )
        elif option.style == OptionStyle.AMERICAN:
            if option.option_type == OptionType.CALL:
                price = fdp.price_american_call(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )
            else:
                price = fdp.price_american_put(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )
        else:
            # Bermudan - use American as approximation for now
            if option.option_type == OptionType.CALL:
                price = fdp.price_american_call(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )
            else:
                price = fdp.price_american_put(
                    spot, option.strike, params.rate, params.div_yield,
                    params.vol, T, gp.n_space, gp.n_time
                )

        # Calculate Greeks via finite differences
        greeks = self._calculate_greeks(fdp, option, spot, T, params, gp, price)

        return PricingResult(
            price=price,
            greeks=greeks,
            model_type="GBM",
            grid_points=gp.n_space,
            time_steps=gp.n_time,
        )

    def _calculate_greeks(
        self,
        fdp: FDPricing,
        option: Option,
        spot: float,
        T: float,
        params: ModelParams,
        gp: GridParams,
        price: float,
    ) -> Greeks:
        """Calculate Greeks via finite differences."""
        from quiver.domain.option import OptionStyle, OptionType

        # Bump sizes
        ds = spot * 0.01  # 1% spot bump
        dv = 0.01  # 1% vol bump
        dt = 1.0 / 365.0  # 1 day

        # Select pricing function
        def price_fn(s: float, v: float, t: float) -> float:
            if option.style == OptionStyle.EUROPEAN:
                if option.option_type == OptionType.CALL:
                    return fdp.price_european_call(
                        s, option.strike, params.rate, params.div_yield,
                        v, t, gp.n_space, gp.n_time
                    )
                else:
                    return fdp.price_european_put(
                        s, option.strike, params.rate, params.div_yield,
                        v, t, gp.n_space, gp.n_time
                    )
            else:  # American
                if option.option_type == OptionType.CALL:
                    return fdp.price_american_call(
                        s, option.strike, params.rate, params.div_yield,
                        v, t, gp.n_space, gp.n_time
                    )
                else:
                    return fdp.price_american_put(
                        s, option.strike, params.rate, params.div_yield,
                        v, t, gp.n_space, gp.n_time
                    )

        # Delta and Gamma via central differences
        price_up = price_fn(spot + ds, params.vol, T)
        price_down = price_fn(spot - ds, params.vol, T)
        delta = (price_up - price_down) / (2 * ds)
        gamma = (price_up - 2 * price + price_down) / (ds * ds)

        # Theta (using forward difference, negative because time decreases)
        if T > dt:
            price_t_down = price_fn(spot, params.vol, T - dt)
            theta = (price_t_down - price) / dt  # Already per day
        else:
            theta = 0.0

        # Vega (per 1% vol move)
        price_v_up = price_fn(spot, params.vol + dv, T)
        vega = (price_v_up - price) / dv * 0.01  # Scale to per 1% move

        return Greeks(
            delta=delta,
            gamma=gamma,
            theta=theta,
            vega=vega,
            rho=0.0,  # TODO: Implement rho calculation
        )

    def price_batch(
        self,
        options: Sequence[Option],
        spots: Sequence[float],
        params: Sequence[ModelParams],
        grid_params: GridParams | None = None,
    ) -> list[PricingResult]:
        """Price multiple options.

        Args:
            options: Options to price
            spots: Spot prices for each option
            params: Model parameters for each option
            grid_params: Optional grid parameters

        Returns:
            List of PricingResult for each option
        """
        return [
            self.price(opt, spot, p, grid_params)
            for opt, spot, p in zip(options, spots, params)
        ]


# Type alias for the CFFI wrapper (avoids circular import at runtime)
if TYPE_CHECKING:
    from quiver.bindings.fdpricing import FDPricing
else:
    FDPricing = None
