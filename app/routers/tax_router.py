"""Tax calculation API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tax_schema import TaxCalculationRequest, TaxCalculationResponse
from app.services import get_tax_calculation, get_tax_history

router = APIRouter()

@router.post(
    "/calculate",
    response_model=TaxCalculationResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate income tax for Old and New regimes",
)
async def calculate_tax(payload: TaxCalculationRequest, db: Session = Depends(get_db)) -> TaxCalculationResponse:
    """Calculate tax under Old and New regimes."""
    return await get_tax_calculation(payload, db)


@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Get all tax calculation records",
)
def fetch_tax_history(db: Session = Depends(get_db)):
    """Retrieve all tax calculation records stored in DB."""
    return get_tax_history(db)
