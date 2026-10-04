# DemandSense Test Suite

This directory contains integration and end-to-end tests for DemandSense.

## Structure

- `test_project_structure.py`: Validates foundational project directory compliance.
- `backend/tests/`: Unit and API integration tests for FastAPI backend services.
- Later phases will add:
  - `ml/tests/`: Unit tests for feature extraction and forecasting models.
  - `integration/`: Multi-service integration tests.

## Running Tests

Run all tests:
```bash
python -m pytest
```

Run backend tests specifically:
```bash
python -m pytest backend/tests
```
