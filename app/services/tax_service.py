"""Tax calculation service."""

import asyncio
from sqlalchemy.orm import Session

from app.exceptions import ValidationError
from app.models.tax_record import TaxRecord
from app.repository import create_tax_record, get_all_tax_records
from app.schemas.tax_schema import TaxCalculationRequest, TaxCalculationResponse
from app.utils import calculate_new_regime_tax, calculate_old_regime_tax


async def get_tax_calculation(payload: TaxCalculationRequest, db: Session) -> TaxCalculationResponse:
    """Compute tax for Old and New regimes."""
    if payload.total_deductions > payload.gross_income:
        raise ValidationError("Total deductions cannot exceed total gross annual income.")

    old_regime, new_regime = await asyncio.gather(
        calculate_old_regime_tax(
            gross_income=payload.gross_income,
            is_salaried=payload.is_salaried,
            total_deductions=payload.total_deductions,
        ),
        calculate_new_regime_tax(
            gross_income=payload.gross_income,
            is_salaried=payload.is_salaried,
        ),
    )

    if new_regime.total_tax < old_regime.total_tax:
        recommended_regime = "New Tax Regime"
        savings = round(old_regime.total_tax - new_regime.total_tax, 2)
        message = f"New Tax Regime saves you ₹{savings:,.2f} compared to Old Tax Regime."
    elif old_regime.total_tax < new_regime.total_tax:
        recommended_regime = "Old Tax Regime"
        savings = round(new_regime.total_tax - old_regime.total_tax, 2)
        message = f"Old Tax Regime saves you ₹{savings:,.2f} compared to New Tax Regime."
    else:
        recommended_regime = "New Tax Regime"
        savings = 0.0
        message = "Both tax regimes result in the same tax."

    create_tax_record(db, payload, old_regime.total_tax, new_regime.total_tax)

    return TaxCalculationResponse(
        gross_income=payload.gross_income,
        old_regime=old_regime,
        new_regime=new_regime,
        recommended_regime=recommended_regime,
        tax_savings=savings,
        message=message,
    )


def get_tax_history(db: Session) -> list[TaxRecord]:
    """Retrieve tax calculation records."""
    return get_all_tax_records(db)
