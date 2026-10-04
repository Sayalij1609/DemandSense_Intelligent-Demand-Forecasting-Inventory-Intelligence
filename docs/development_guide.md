# DemandSense Development Guide

This guide details local environment setup, testing procedures, and best practices.

## Prerequisites

- **Python**: 3.11+ (Python 3.12 recommended)
- **Node.js**: 20+ (Node v22 recommended)
- **Docker & Docker Compose**: Optional for containerized workflow

---

## 1. Local Backend Setup

1. Open a terminal in the project root:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
4. Copy the environment configuration:
   ```bash
   cp .env.example .env
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. Visit [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## 2. Local Frontend Setup

1. Open a new terminal in the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173).

---

## 3. Running with Docker Compose

To spin up all services (PostgreSQL, FastAPI Backend, React Frontend):
```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

---

## 4. Running Tests

Run the test suite from the repository root:
```bash
python -m pytest
```
Run backend tests specifically:
```bash
python -m pytest backend/tests
```
