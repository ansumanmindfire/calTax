"""Repository package exports."""

from app.repository.tax_repository import create_tax_record, get_all_tax_records

__all__ = [
    "create_tax_record",
    "get_all_tax_records",
]
