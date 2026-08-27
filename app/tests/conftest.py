"""Pytest fixtures and configuration."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.tax_record import Base
from app.schemas.tax_schema import TaxCalculationRequest


@pytest.fixture
def db_session() -> Session:
    """Provide an isolated in-memory SQLite database session for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def sample_tax_request_salaried() -> TaxCalculationRequest:
    """Fixture for standard salaried tax request."""
    return TaxCalculationRequest(
        gross_income=1200000.0,
        is_salaried=True,
        age=28,
        total_deductions=150000.0,
    )