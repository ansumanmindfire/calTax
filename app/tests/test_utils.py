"""Unit tests for tax calculation utility functions."""

from app.constants import (
    OLD_REGIME_STANDARD_DEDUCTION,
    NEW_REGIME_STANDARD_DEDUCTION,
    OLD_REGIME_SLABS,
    NEW_REGIME_SLABS,
)
from app.utils.tax_utils import (
    _compute_base_tax_from_slabs,
    calculate_new_regime_tax,
    calculate_old_regime_tax,
)


def test_base_tax_zero_taxable_slab_old_regime():
    """Test that base tax is 0 when income falls within zero tax bracket."""

    base_tax = _compute_base_tax_from_slabs(200000.0, OLD_REGIME_SLABS)
    assert base_tax == 0.0


def test_base_tax_zero_taxable_slab_new_regime():
    """Test that base tax is 0 when income falls within zero tax bracket."""

    base_tax = _compute_base_tax_from_slabs(200000.0, NEW_REGIME_SLABS)
    assert base_tax == 0.0


def test_compute_base_tax_old_regime():
    """Test tax calculation across multiple slab."""

    base_tax = _compute_base_tax_from_slabs(600000.0, OLD_REGIME_SLABS)
    assert base_tax == 32500.0


def test_compute_base_tax_new_regime():
    """Test tax calculation across multiple slabs."""

    base_tax = _compute_base_tax_from_slabs(600000.0, NEW_REGIME_SLABS)
    assert base_tax == 10000.0


async def test_calculate_old_regime_tax_salaried():
    """Test Old Regime tax with standard deduction and general deductions."""

    gross = 1000000.0
    deductions = 150000.0

    result = await calculate_old_regime_tax(
        gross_income=gross,
        is_salaried=True,
        total_deductions=deductions,
    )

    assert result.taxable_income == 800000.0
    assert result.standard_deduction == OLD_REGIME_STANDARD_DEDUCTION
    assert result.total_deductions == deductions
    assert result.base_tax == 72500.0
    assert result.cess == 2900.0
    assert result.total_tax == 75400.0


async def test_calculate_old_regime_tax_non_salaried():
    """Test Old Regime tax without standard deduction for non-salaried users."""

    gross = 500000.0
    deductions = 50000.0

    result = await calculate_old_regime_tax(
        gross_income=gross,
        is_salaried=False,
        total_deductions=deductions,
    )

    assert result.standard_deduction == 0.0
    assert result.taxable_income == 450000.0
    assert result.base_tax == 10000.0
    assert result.cess == 400.0
    assert result.total_tax == 10400.0


async def test_calculate_new_regime_tax_salaried():
    """Test New Regime tax computation for salaried users."""

    gross = 1200000.0

    result = await calculate_new_regime_tax(
        gross_income=gross,
        is_salaried=True,
    )

    assert result.standard_deduction == NEW_REGIME_STANDARD_DEDUCTION
    assert result.total_deductions == 0.0
    assert result.taxable_income == 1125000.0
    assert result.base_tax == 52500.0
    assert result.cess == 2100.0
    assert result.total_tax == 54600.0


async def test_calculate_new_regime_tax_non_salaried():
    """Test New Regime tax computation for non-salaried users."""
    
    gross = 600000.0

    result = await calculate_new_regime_tax(
        gross_income=gross,
        is_salaried=False,
    )

    assert result.standard_deduction == 0.0
    assert result.taxable_income == 600000.0
    assert result.base_tax == 10000.0
    assert result.cess == 400.0
    assert result.total_tax == 10400.0
