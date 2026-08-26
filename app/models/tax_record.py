from sqlalchemy import DateTime, Boolean, String, Integer, Float, Column
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class TaxRecord(Base):

    __tablename__ = "tax_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gross_income = Column(Float, nullable=False)
    is_salaried = Column(Boolean, nullable=False)
    age = Column(Integer, default=22)
    total_deductions = Column(Float, default=0.0)

    old_regime_tax = Column(Float, nullable=False)
    new_regime_tax = Column(Float, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
