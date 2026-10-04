"""Health check endpoint handler."""
from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    description="Returns the current operational status, environment, and version of the API.",
)
async def check_health() -> HealthResponse:
    """Check application operational status and metadata."""
    return HealthResponse(
        status="healthy",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        services={
            "api": "up",
            "database": "configured",
        },
    )
