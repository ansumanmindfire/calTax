"""Environment configuration loader for calTax application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Load and expose environment settings for the application."""

    def __init__(self) -> None:
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEVELOPMENT")

        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "caltax")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
        self.PROJECT_DESCRIPTION: str = os.getenv(
            "PROJECT_DESCRIPTION",
            "Income Tax Calculator and Regime Recommendation API",
        )

        self.PORT: int = int(os.getenv("PORT", "8000"))

        self.LOG_DIR: str = os.getenv("LOG_DIR", "logs")

        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL", "sqlite:///./tax_calculator.db"
        )


# Global singleton settings instance
settings = Settings()