# DemandSense API Reference

The DemandSense backend provides RESTful JSON endpoints under the `/api/v1` namespace.

Interactive OpenAPI documentation is available when running the server:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## Endpoints

### 1. Root Information

- **Method**: `GET`
- **Path**: `/`
- **Description**: Returns top-level service metadata and navigation links.

#### Response `200 OK`
```json
{
  "name": "DemandSense API",
  "version": "0.1.0",
  "status": "online",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

---

### 2. Service Health Check

- **Method**: `GET`
- **Path**: `/api/v1/health`
- **Description**: Verifies operational readiness and service statuses.

#### Response `200 OK`
```json
{
  "status": "healthy",
  "app_name": "DemandSense API",
  "version": "0.1.0",
  "environment": "development",
  "timestamp": "2026-10-04T14:30:00.000000Z",
  "services": {
    "api": "up",
    "database": "configured"
  }
}
```
