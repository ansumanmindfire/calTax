"""Tax calculation API router."""

from typing import Union
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tax_schema import (
    CalculationMode,
    SingleRegimeResponse,
    TaxCalculationRequest,
    TaxCalculationResponse,
)
from app.services import get_tax_calculation, get_tax_history

router = APIRouter()


@router.post(
    "/calculate",
    response_model=Union[TaxCalculationResponse, SingleRegimeResponse],
    status_code=status.HTTP_200_OK,
    summary="Calculate income tax for Old, New, or Compare both regimes",
)
async def calculate_tax(
    payload: TaxCalculationRequest,
    mode: CalculationMode = Query(
        default=CalculationMode.COMPARE,
        description="Calculation mode: 'new', 'old', or 'compare'",
    ),
    db: Session = Depends(get_db),
) -> Union[TaxCalculationResponse, SingleRegimeResponse]:
    """Calculate tax for Old Regime, New Regime, or comparison mode.

    Args:
        payload: Income details, employment status, and deductions.
        mode: Calculation mode ('compare', 'old', or 'new').
        db: Database session dependency.

    Returns:
        TaxCalculationResponse or SingleRegimeResponse: Tax calculation result.
    """
    return await get_tax_calculation(payload=payload, db=db, mode=mode)


@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Get all tax calculation records",
)
def fetch_tax_history(db: Session = Depends(get_db)):
    """Retrieve all historical tax calculation records.

    Args:
        db: Database session dependency.

    Returns:
        list[TaxRecord]: List of stored tax calculation records.
    """
    return get_tax_history(db)

