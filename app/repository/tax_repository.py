"""Tax repository for database operations."""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import logger
from app.exceptions import InternalError
from app.models.tax_record import TaxRecord
from app.schemas.tax_schema import TaxCalculationRequest


def create_tax_record(
    db: Session,
    payload: TaxCalculationRequest,
    old_regime_tax: float,
    new_regime_tax: float,
) -> TaxRecord:
    """Create a new tax calculation record."""
    tax_record = TaxRecord(
        gross_income=payload.gross_income,
        is_salaried=payload.is_salaried,
        age=payload.age,
        total_deductions=payload.total_deductions,
        old_regime_tax=old_regime_tax,
        new_regime_tax=new_regime_tax,
    )
    try:
        db.add(tax_record)
        db.commit()
        db.refresh(tax_record)
        return tax_record
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception(f"Database error during create_tax_record: {str(exc)}")
        raise InternalError("Failed to save tax record to database.") from exc


def get_all_tax_records(db: Session) -> list[TaxRecord]:
    """Retrieve all tax calculation records."""
    try:
        records = db.query(TaxRecord).all()
        return records
    except SQLAlchemyError as exc:
        logger.exception(f"Database error during get_all_tax_records: {str(exc)}")
        raise InternalError("Failed to retrieve tax records from database.") from exc
