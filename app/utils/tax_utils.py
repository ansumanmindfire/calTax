"""Tax calculation utility functions."""

from app.constants import (
    CESS_RATE,
    NEW_REGIME_SLABS,
    NEW_REGIME_STANDARD_DEDUCTION,
    OLD_REGIME_SLABS,
    OLD_REGIME_STANDARD_DEDUCTION,
)
from app.schemas.tax_schema import Regime


def _compute_base_tax_from_slabs(
    taxable_income: float,
    slabs: list[tuple[float, float, float]],
) -> float:
    """Calculate base tax."""
    base_tax = 0.0
    for lower, upper, rate in slabs:
        if taxable_income > lower:
            taxable_chunk = min(taxable_income, upper) - lower
            base_tax += taxable_chunk * rate
    return base_tax


async def calculate_old_regime_tax(
    gross_income: float,
    is_salaried: bool,
    total_deductions: float,
) -> Regime:
    """Calculate tax breakdown under the Old Tax Regime."""
    standard_deduction = OLD_REGIME_STANDARD_DEDUCTION if is_salaried else 0.0
    taxable_income = max(0.0, gross_income - standard_deduction - total_deductions)

    base_tax = _compute_base_tax_from_slabs(taxable_income, OLD_REGIME_SLABS)
    cess = round(base_tax * CESS_RATE, 2)
    total_tax = round(base_tax + cess, 2)

    return Regime(
        taxable_income=round(taxable_income, 2),
        standard_deduction=round(standard_deduction, 2),
        total_deductions=round(total_deductions, 2),
        base_tax=round(base_tax, 2),
        cess=cess,
        total_tax=total_tax,
    )


async def calculate_new_regime_tax(
    gross_income: float,
    is_salaried: bool,
) -> Regime:
    """Calculate tax breakdown under the New Tax Regime."""
    standard_deduction = NEW_REGIME_STANDARD_DEDUCTION if is_salaried else 0.0
    taxable_income = max(0.0, gross_income - standard_deduction)

    base_tax = _compute_base_tax_from_slabs(taxable_income, NEW_REGIME_SLABS)
    cess = round(base_tax * CESS_RATE, 2)
    total_tax = round(base_tax + cess, 2)

    return Regime(
        taxable_income=round(taxable_income, 2),
        standard_deduction=round(standard_deduction, 2),
        total_deductions=0.0,
        base_tax=round(base_tax, 2),
        cess=cess,
        total_tax=total_tax,
    )
