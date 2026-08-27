"""Tax constants for Old and New Tax Regimes"""

# Standard Deductions
OLD_REGIME_STANDARD_DEDUCTION = 50000.0
NEW_REGIME_STANDARD_DEDUCTION = 75000.0

# 4% Health & Education Cess
CESS_RATE = 0.04

# Old Tax Regime Slabs: (lower_limit, upper_limit, tax_rate)
OLD_REGIME_SLABS: list[tuple[float, float, float]] = [
    (0.0, 250000.0, 0.00),
    (250000.0, 500000.0, 0.05),
    (500000.0, 1000000.0, 0.20),
    (1000000.0, float("inf"), 0.30),
]

# New Tax Regime Slabs (FY 2025-26): (lower_limit, upper_limit, tax_rate)
NEW_REGIME_SLABS: list[tuple[float, float, float]] = [
    (0.0, 400000.0, 0.00),
    (400000.0, 800000.0, 0.05),
    (800000.0, 1200000.0, 0.10),
    (1200000.0, 1600000.0, 0.15),
    (1600000.0, 2000000.0, 0.20),
    (2000000.0, 2400000.0, 0.25),
    (2400000.0, float("inf"), 0.30),
]
