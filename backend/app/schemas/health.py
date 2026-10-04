"""Health check response schema."""
from datetime import datetime, timezone
from typing import Dict, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Structured health check status response."""

    status: str = Field(default="healthy", description="Application service status")
    app_name: str = Field(description="Name of the running application")
    version: str = Field(description="Semantic version of the application")
    environment: str = Field(description="Current deployment environment")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Current UTC timestamp",
    )
    services: Optional[Dict[str, str]] = Field(
        default_factory=lambda: {"api": "up"},
        description="Status of connected services",
    )
