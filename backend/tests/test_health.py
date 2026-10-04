"""Tests for health check endpoints."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify root endpoint returns 200 and valid payload."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data
    assert "health" in data


def test_health_check_endpoint():
    """Verify /api/v1/health returns 200 and healthy status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "DemandSense API"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
    assert data["services"]["api"] == "up"
