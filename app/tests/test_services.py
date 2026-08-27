"""Unit tests for the tax service layer."""

import pytest
from app.exceptions import ValidationError
from app.schemas.tax_schema import (
    CalculationMode,
    SingleRegimeResponse,
    TaxCalculationRequest,
    TaxCalculationResponse,
)
from app.services.tax_service import get_tax_calculation, get_tax_history


async def test_deductions_exceed_gross(db_session):
    """Test that deductions higher than gross income raises ValidationError."""

    payload = TaxCalculationRequest(
        gross_income=500000.0,
        total_deductions=600000.0,
    )
    with pytest.raises(ValidationError) as exc:
        await get_tax_calculation(payload, db_session)

    assert "Total deductions cannot exceed total gross annual income." == str(exc.value.message)


async def test_get_tax_calculation_mode_new(db_session):
    """Test calculation specifically for New Tax Regime mode."""

    payload = TaxCalculationRequest(
        gross_income=1200000.0,
        is_salaried=True,
    )

    response = await get_tax_calculation(payload, db_session, mode=CalculationMode.NEW)

    assert isinstance(response, SingleRegimeResponse)
    assert response.regime == "New Tax Regime"
    assert response.gross_income == 1200000.0
    assert response.details.standard_deduction == 75000.0
    assert response.details.total_tax == 54600.0


async def test_get_tax_calculation_mode_old(db_session):
    """Test calculation specifically for Old Tax Regime mode."""

    payload = TaxCalculationRequest(
        gross_income=1000000.0,
        is_salaried=True,
        total_deductions=150000.0,
    )

    response = await get_tax_calculation(payload, db_session, mode=CalculationMode.OLD)

    assert isinstance(response, SingleRegimeResponse)
    assert response.regime == "Old Tax Regime"
    assert response.gross_income == 1000000.0
    assert response.details.standard_deduction == 50000.0
    assert response.details.total_deductions == 150000.0
    assert response.details.total_tax == 75400.0


async def test_old_deductions_exceed(db_session):
    """Test that Old Tax Regime mode also validates deductions."""
    payload = TaxCalculationRequest(
        gross_income=400000.0,
        total_deductions=500000.0,
    )
    with pytest.raises(ValidationError) as exc:
        await get_tax_calculation(payload, db_session, mode=CalculationMode.OLD)

    assert "Total deductions cannot exceed total gross annual income." == str(exc.value.message)


async def test_get_tax_calculation_recommends_new_regime(db_session):
    """Test standard case where New Tax Regime is more beneficial in COMPARE mode."""
    
    payload = TaxCalculationRequest(
        gross_income=1200000.0,
        is_salaried=True,
        total_deductions=50000.0,
    )

    response = await get_tax_calculation(payload, db_session, mode=CalculationMode.COMPARE)

    assert isinstance(response, TaxCalculationResponse)
    assert response.recommended_regime == "New Tax Regime"
    assert response.new_regime.total_tax < response.old_regime.total_tax
    assert response.tax_savings > 0
    assert "New Tax Regime saves you" in response.message

    # Verify that database record was created
    history = get_tax_history(db_session)
    assert len(history) == 1
    assert history[0].gross_income == 1200000.0


async def test_get_tax_calculation_recommends_old_regime(db_session):
    """Test case where high deductions make Old Tax Regime more beneficial."""

    payload = TaxCalculationRequest(
        gross_income=1000000.0,
        is_salaried=True,
        total_deductions=400000.0,
    )

    response = await get_tax_calculation(payload, db_session)

    assert isinstance(response, TaxCalculationResponse)
    assert response.recommended_regime == "Old Tax Regime"
    assert response.old_regime.total_tax < response.new_regime.total_tax
    assert response.tax_savings > 0
    assert "Old Tax Regime saves you" in response.message

    # Verify that database record was created
    history = get_tax_history(db_session)
    assert len(history) == 1
    assert history[0].gross_income == 1000000.0


async def test_get_tax_calculation_both_regimes_equal(db_session):
    """Test case where both regimes have identical tax payable."""

    payload = TaxCalculationRequest(
        gross_income=200000.0,
        is_salaried=False,
        total_deductions=0.0,
    )

    response = await get_tax_calculation(payload, db_session)

    assert isinstance(response, TaxCalculationResponse)
    assert response.recommended_regime == "New Tax Regime"
    assert response.tax_savings == 0.0
    assert response.message == "Both tax regimes result in the same tax."


async def test_get_tax_history(db_session):
    """Test retrieving tax calculation history."""
    
    payload1 = TaxCalculationRequest(gross_income=600000.0)
    payload2 = TaxCalculationRequest(gross_income=1000000.0)

    await get_tax_calculation(payload1, db_session)
    await get_tax_calculation(payload2, db_session)

    records = get_tax_history(db_session)
    assert len(records) == 2
    assert records[0].gross_income == 600000.0
    assert records[1].gross_income == 1000000.0
