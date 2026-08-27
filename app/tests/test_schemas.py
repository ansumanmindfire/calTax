"""Unit tests for Pydantic request and response schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.tax_schema import (
    CalculationMode,
    Regime,
    SingleRegimeResponse,
    TaxCalculationRequest,
    TaxCalculationResponse,
)


def test_tax_calculation_request_defaults():
    """Test creating TaxCalculationRequest with minimal required fields."""

    request = TaxCalculationRequest(gross_income=500000.0)
    assert request.gross_income == 500000.0
    assert request.is_salaried is True
    assert request.age == 22
    assert request.total_deductions == 0.0


def test_tax_calculation_request_custom_values():
    """Test creating TaxCalculationRequest with custom valid parameters."""

    request = TaxCalculationRequest(
        gross_income=1500000.0,
        is_salaried=False,
        age=45,
        total_deductions=200000.0,
    )
    assert request.gross_income == 1500000.0
    assert request.is_salaried is False
    assert request.age == 45
    assert request.total_deductions == 200000.0


def test_tax_calculation_request_invalid_gross_income():
    """Test that gross_income <= 0 raises validation error."""

    with pytest.raises(ValidationError):
        TaxCalculationRequest(gross_income=0.0)

    with pytest.raises(ValidationError):
        TaxCalculationRequest(gross_income=-50000.0)


def test_tax_calculation_request_invalid_age():
    """Test that age outside [0, 100] raises validation error."""
    
    with pytest.raises(ValidationError):
        TaxCalculationRequest(gross_income=500000.0, age=-1)

    with pytest.raises(ValidationError):
        TaxCalculationRequest(gross_income=500000.0, age=101)


def test_tax_calculation_request_invalid_deductions():
    """Test that negative deductions raise validation error."""

    with pytest.raises(ValidationError):
        TaxCalculationRequest(gross_income=500000.0, total_deductions=-1000.0)


def test_calculation_mode_enum():
    """Test CalculationMode enum values."""
    assert CalculationMode.NEW.value == "new"
    assert CalculationMode.OLD.value == "old"
    assert CalculationMode.COMPARE.value == "compare"


def test_single_regime_response_schema():
    """Test construction of SingleRegimeResponse model."""
    regime = Regime(
        taxable_income=725000.0,
        standard_deduction=75000.0,
        total_deductions=0.0,
        base_tax=16250.0,
        cess=650.0,
        total_tax=16900.0,
    )
    single_res = SingleRegimeResponse(
        gross_income=800000.0,
        regime="New Tax Regime",
        details=regime,
    )
    assert single_res.gross_income == 800000.0
    assert single_res.regime == "New Tax Regime"
    assert single_res.details.total_tax == 16900.0


def test_regime_and_response_schema():
    """Test construction of Regime and TaxCalculationResponse models."""

    old_regime = Regime(
        taxable_income=750000.0,
        standard_deduction=50000.0,
        total_deductions=100000.0,
        base_tax=62500.0,
        cess=2500.0,
        total_tax=65000.0,
    )
    new_regime = Regime(
        taxable_income=825000.0,
        standard_deduction=75000.0,
        total_deductions=0.0,
        base_tax=22500.0,
        cess=900.0,
        total_tax=23400.0,
    )

    response = TaxCalculationResponse(
        gross_income=900000.0,
        old_regime=old_regime,
        new_regime=new_regime,
        recommended_regime="New Tax Regime",
        tax_savings=41600.0,
        message="New Tax Regime saves you ₹41,600.00 compared to Old Tax Regime.",
    )

    assert response.gross_income == 900000.0
    assert response.recommended_regime == "New Tax Regime"
    assert response.tax_savings == 41600.0
