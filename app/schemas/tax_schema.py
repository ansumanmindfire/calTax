"""Tax calculation Pydantic request and response schemas."""

from enum import Enum
from pydantic import BaseModel, Field


class CalculationMode(str, Enum):
    """Tax calculation mode options for API queries."""

    NEW = "new"
    OLD = "old"
    COMPARE = "compare"


class TaxCalculationRequest(BaseModel):
    """Input payload for tax calculation."""

    gross_income: float = Field(
        ...,
        gt=0,
        description="Total annual gross income in INR"
    )
    is_salaried: bool = Field(
        default=True,
        description="Whether the taxpayer is a salaried individual"
    )
    age: int = Field(
        default=22,
        ge=0,
        le=100,
        description="Age of the taxpayer"
    )
    total_deductions: float = Field(
        default=0.0,
        ge=0,
        description="Total deductions"
    )


class Regime(BaseModel):
    """Detailed tax computation breakdown."""

    taxable_income: float = Field(
        ...,
        description="Net taxable income after all deductions",
    )
    standard_deduction: float = Field(
        ...,
        description="Standard deduction applied"
    )
    total_deductions: float = Field(
        ...,
        description="Total deductions applied, if applicable",
    )
    base_tax: float = Field(
        ...,
        description="Base tax before cess",
    )
    cess: float = Field(
        ...,
        description="4% Health & Education Cess",
    )
    total_tax: float = Field(
        ...,
        description="Final tax payable (base_tax + cess)",
    )


class SingleRegimeResponse(BaseModel):
    """Response when calculating for a single regime (new or old)."""

    gross_income: float = Field(
        ...,
        description="Gross income provided by the user",
    )
    regime: str = Field(
        ...,
        description="Calculated regime name",
    )
    details: Regime = Field(
        ...,
        description="Detailed tax computation breakdown",
    )


class TaxCalculationResponse(BaseModel):
    """Response after tax calculation and comparison."""

    gross_income: float = Field(
        ...,
        description="Gross income provided by the user",
    )
    old_regime: Regime = Field(
        ...,
        description="Detailed tax computation under Old Tax Regime",
    )
    new_regime: Regime = Field(
        ...,
        description="Detailed tax computation under New Tax Regime",
    )
    recommended_regime: str = Field(
        ...,
        description="Recommended Regime",
    )
    tax_savings: float = Field(
        ...,
        description="Amount saved by choosing the recommended regime",
    )
    message: str = Field(
        ...,
        description="Recommendation summary message"
    )
