"""Application settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field


class PricingSettings(BaseModel):
    """Pricing engine settings."""

    n_space: int = Field(default=200, ge=10, le=1000, description="Spatial grid points")
    n_time: int = Field(default=100, ge=10, le=1000, description="Time steps")
    grid_type: str = Field(default="sinh", pattern="^(uniform|sinh|log)$")


class ModelSettings(BaseModel):
    """Default model settings."""

    default_rate: float = Field(default=0.05, ge=0, le=1, description="Risk-free rate")
    default_div: float = Field(default=0.02, ge=0, le=1, description="Dividend yield")
    default_vol: float = Field(default=0.20, ge=0.01, le=2, description="Volatility")


class DisplaySettings(BaseModel):
    """Display settings."""

    refresh_on_select: bool = Field(default=True, description="Refresh on position select")
    show_aggregate_greeks: bool = Field(default=True, description="Show aggregate Greeks")
    date_format: str = Field(default="%Y-%m-%d", description="Date display format")


class Settings(BaseModel):
    """Application settings."""

    pricing: PricingSettings = Field(default_factory=PricingSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    display: DisplaySettings = Field(default_factory=DisplaySettings)

    # Paths
    lib_path: Path | None = Field(default=None, description="Path to libfdpricing.so")
    data_dir: Path = Field(
        default=Path.home() / ".local" / "share" / "quiver",
        description="Data directory",
    )
    config_dir: Path = Field(
        default=Path.home() / ".config" / "quiver",
        description="Config directory",
    )

    @classmethod
    def load(cls, path: Path | None = None) -> Self:
        """Load settings from file.

        Args:
            path: Path to config file. If None, uses default location.

        Returns:
            Loaded settings (or defaults if file doesn't exist)
        """
        if path is None:
            path = Path.home() / ".config" / "quiver" / "config.json"

        if not path.exists():
            return cls()

        import json

        with open(path) as f:
            data = json.load(f)
        return cls.model_validate(data)

    def save(self, path: Path | None = None) -> None:
        """Save settings to file.

        Args:
            path: Path to save to. If None, uses default location.
        """
        if path is None:
            path = self.config_dir / "config.json"

        path.parent.mkdir(parents=True, exist_ok=True)

        import json

        with open(path, "w") as f:
            json.dump(self.model_dump(mode="json"), f, indent=2, default=str)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance (loaded from file or defaults)
    """
    return Settings.load()
