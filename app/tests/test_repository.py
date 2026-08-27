"""Unit tests for the repository layer."""

from unittest.mock import MagicMock
import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import InternalError
from app.models.tax_record import TaxRecord
from app.repository.tax_repository import create_tax_record, get_all_tax_records
from app.schemas.tax_schema import TaxCalculationRequest


def test_create_tax_record_success(db_session, sample_tax_request_salaried):
    """Test successfully persisting a tax record to the database."""

    record = create_tax_record(
        db=db_session,
        payload=sample_tax_request_salaried,
        old_regime_tax=75000.0,
        new_regime_tax=54600.0,
    )

    assert record.id is not None
    assert record.created_at is not None
    assert record.gross_income == sample_tax_request_salaried.gross_income
    assert record.is_salaried == sample_tax_request_salaried.is_salaried
    assert record.age == sample_tax_request_salaried.age
    assert record.total_deductions == sample_tax_request_salaried.total_deductions
    assert record.old_regime_tax == 75000.0
    assert record.new_regime_tax == 54600.0


def test_db_error_raises_internal_error(sample_tax_request_salaried):
    """Test that a database failure raises an InternalError exception."""

    mock_db = MagicMock()
    mock_db.commit.side_effect = SQLAlchemyError("DB Connection Lost")

    with pytest.raises(InternalError) as exc:
        create_tax_record(
            db=mock_db,
            payload=sample_tax_request_salaried,
            old_regime_tax=50000.0,
            new_regime_tax=40000.0,
        )

    assert "Failed to save tax record to database." in str(exc.value.message)
    mock_db.rollback.assert_called_once()


def test_get_all_tax_records_success(db_session):
    """Test retrieving all tax records from database."""

    # Initially empty
    records = get_all_tax_records(db_session)
    assert records == []

    # Add records
    req1 = TaxCalculationRequest(gross_income=500000.0)
    req2 = TaxCalculationRequest(gross_income=800000.0)

    create_tax_record(db_session, req1, old_regime_tax=12500.0, new_regime_tax=10000.0)
    create_tax_record(db_session, req2, old_regime_tax=45000.0, new_regime_tax=35000.0)

    all_records = get_all_tax_records(db_session)
    assert len(all_records) == 2
    assert all_records[0].gross_income == 500000.0
    assert all_records[1].gross_income == 800000.0
