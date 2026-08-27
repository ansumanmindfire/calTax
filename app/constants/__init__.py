"""Constants package exports."""

from app.constants.tax_constants import (
    CESS_RATE,
    NEW_REGIME_SLABS,
    NEW_REGIME_STANDARD_DEDUCTION,
    OLD_REGIME_SLABS,
    OLD_REGIME_STANDARD_DEDUCTION,
)

__all__ = [
    "OLD_REGIME_STANDARD_DEDUCTION",
    "NEW_REGIME_STANDARD_DEDUCTION",
    "CESS_RATE",
    "OLD_REGIME_SLABS",
    "NEW_REGIME_SLABS",
]
