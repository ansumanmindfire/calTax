"""Utils package exports."""

from app.utils.tax_utils import calculate_new_regime_tax, calculate_old_regime_tax

__all__ = [
    "calculate_old_regime_tax",
    "calculate_new_regime_tax",
]
