"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import logger, settings
from app.exceptions import (
    AppError,
    app_error_handler,
    global_exception_handler,
    http_exception_handler,
    request_validation_handler,
    cancelled_error_handler
)
import asyncio

from app.database import engine
from app.models.tax_record import Base

Base.metadata.create_all(bind=engine)

logger.info("Initializing FastAPI application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

# Register Global Exception Handlers
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(asyncio.CancelledError, cancelled_error_handler)


@app.get("/")
def home():
    """Health / root probe endpoint."""
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}