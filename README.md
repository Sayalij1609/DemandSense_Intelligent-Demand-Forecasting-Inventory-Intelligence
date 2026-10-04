# DemandSense — Intelligent Demand Forecasting & Inventory Intelligence

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PyTorch](https://img.shields.io/badge/ML-PyTorch%20%7C%20LightGBM%20%7C%20XGBoost-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/DevOps-Docker%20%26%20Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

DemandSense is a production-grade machine learning system designed to forecast SKU-level customer demand across time horizons and automatically translate probabilistic forecasts into optimal inventory replenishment decisions.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Inventory Decision Outputs](#inventory-decision-outputs)
3. [End-to-End System Architecture](#end-to-end-system-architecture)
4. [Technology Stack](#technology-stack)
5. [Directory Structure Explained](#directory-structure-explained)
6. [Getting Started & Development Instructions](#getting-started--development-instructions)
7. [Running Tests](#running-tests)
8. [Docker Compose Deployment](#docker-compose-deployment)
9. [Roadmap](#roadmap)

---

## Project Overview

Traditional inventory management relies on static min/max thresholds or simple moving averages, leading to costly stockouts or bloated carrying costs. **DemandSense** bridges the gap between state-of-the-art predictive modeling and supply chain operations.

### Key Capabilities:
- **Multivariate Time-Series Forecasting**: Combines point-of-sale patterns, seasonal trends, price elasticity, and promotional campaigns.
- **Probabilistic Forecasting**: Produces prediction intervals ($P_{10}$, $P_{50}$, $P_{90}$) instead of single-point estimates.
- **Automated Inventory Decisions**: Translates demand distributions directly into dynamic safety stocks, reorder points, and economic order quantities.

---

## Inventory Decision Outputs

The intelligence engine computes the following core operational metrics for each product SKU:

| Metric | Description | Purpose |
| :--- | :--- | :--- |
| **Expected Demand** | Point forecast of anticipated sales over the planning lead time. | Baseline procurement planning. |
| **Demand Trend** | Quantitative trajectory (accelerating, steady, decaying). | Strategic purchasing signals. |
| **Forecast Uncertainty** | Quantile interval dispersion ($P_{90} - P_{10}$) capturing volatility. | Risk-aware hedging. |
| **Safety Stock** | Buffer inventory calculated from demand uncertainty & supplier lead-time variance. | Protection against supply/demand shocks. |
| **Reorder Point (ROP)** | Inventory threshold ($Expected\ Demand_{lead\_time} + Safety\ Stock$). | Automated replenishment triggers. |
| **Stockout Risk** | Probability of running out of inventory before order replenishment. | Prioritizing emergency reorders. |
| **Overstock Risk** | Probability that ending inventory exceeds maximum holding capacity. | Preventing margin erosion & waste. |
| **Recommended Order Quantity (ROQ)** | Optimal order quantity balancing ordering costs against holding costs. | Execution-ready purchase orders. |

---

## End-to-End System Architecture

The planned system comprises 16 sequential architectural stages:

1. **Data Collection & Dataset Integration**: Ingestion of historical sales, promotional calendars, catalog attributes, and supplier lead times.
2. **ETL / Data Preprocessing**: Missing value imputation, calendar standardization, timezone harmonization, and outlier mitigation.
3. **Exploratory Data Analysis (EDA)**: Seasonality decomposition, auto-correlation analysis (ACF/PACF), and SKU velocity segmentation.
4. **Time-Series Feature Engineering**: Lags, rolling window statistics (mean, std, min, max, EWMA), date signals, and promotional indicators.
5. **Traditional ML Forecasting**: Ridge/Lasso, Random Forests, LightGBM, and XGBoost regressor pipelines.
6. **Deep Learning Forecasting**: Sequence-to-sequence architectures using PyTorch (LSTM, GRU, and Temporal Fusion Transformers).
7. **Model Evaluation & Benchmarking**: Expanding and rolling-window backtesting across MAE, RMSE, WAPE, and SMAPE.
8. **Hybrid Ensemble Forecasting**: Error-weighted stacking combining gradient boosting and deep recurrent models.
9. **Forecast Uncertainty Estimation**: Quantile regression and conformal prediction for calibrated confidence bands.
10. **Inventory Intelligence**: Business rule optimization mapping uncertainty to safety stock, ROP, stockout risk, and ROQ.
11. **PostgreSQL Database**: Relational storage for transactions, SKU catalog, forecast snapshots, and recommendation audits.
12. **FastAPI Backend**: Asynchronous RESTful service with Pydantic v2 schemas and SQLAlchemy 2.0 ORM.
13. **React Frontend**: Modern Vite SPA with Tailwind CSS styling and Recharts interactive time-series visualizations.
14. **Testing Suite**: Automated testing with Pytest covering structure, schemas, endpoints, and ML models.
15. **Docker Infrastructure**: Multi-stage container builds for backend, frontend, and PostgreSQL.
16. **Production Deployment**: Cloud-ready configuration, container orchestration, and monitoring.

---

## Technology Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL
- **Machine Learning**: Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, PyTorch
- **Frontend**: React 18, Vite, Tailwind CSS, Recharts, Lucide React
- **DevOps & Tooling**: Docker, Docker Compose, Git, Pytest, Ruff

---

## Directory Structure Explained

```
DemandSense/
├── backend/                  # FastAPI web service & database layer
│   ├── app/
│   │   ├── api/              # API router definitions & versioning (v1)
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   └── health.py # Health check endpoint (/api/v1/health)
│   │   │       └── api.py    # Master router grouping
│   │   ├── core/             # Configuration, settings & environment loaders
│   │   │   └── config.py
│   │   ├── db/               # SQLAlchemy engine & session maker
│   │   │   └── session.py
│   │   ├── models/           # SQLAlchemy ORM entity models
│   │   ├── schemas/          # Pydantic validation models
│   │   │   └── health.py
│   │   ├── services/         # Business logic & orchestrators
│   │   └── main.py           # FastAPI application entrypoint
│   ├── tests/                # Backend unit & integration tests
│   │   └── test_health.py
│   ├── .env.example          # Backend environment template
│   ├── Dockerfile            # Container image specification
│   ├── requirements.txt      # Production backend dependencies
│   └── requirements-dev.txt  # Testing & development tools
│
├── frontend/                 # React single-page application
│   ├── public/               # Static assets & favicon
│   ├── src/
│   │   ├── assets/           # Images & static media
│   │   ├── components/       # Reusable React UI components
│   │   │   └── HealthBadge.jsx
│   │   ├── services/         # API HTTP client services
│   │   │   └── api.js
│   │   ├── App.jsx           # Main application view & dashboard
│   │   ├── index.css         # Tailwind directives & custom CSS
│   │   └── main.jsx          # React DOM entrypoint
│   ├── index.html            # HTML shell with Google Fonts
│   ├── package.json          # Independent npm dependency manifest
│   ├── vite.config.js        # Vite build tool & proxy config
│   ├── tailwind.config.js    # Tailwind theme & design tokens
│   ├── postcss.config.js     # PostCSS configuration
│   ├── .env.example          # Frontend environment template
│   └── Dockerfile            # Container image specification
│
├── ml/                       # Machine learning & inventory engine
│   ├── data/                 # Ingestion connectors & ETL scripts
│   ├── features/             # Time-series feature engineering
│   ├── models/               # Forecasting models (LightGBM, XGBoost, PyTorch)
│   ├── evaluation/           # Backtesting, metrics & benchmarking
│   ├── inventory/            # Inventory optimization & decision logic
│   ├── pipelines/            # Training & inference pipelines
│   ├── requirements.txt      # Independent ML/DS dependencies
│   └── README.md             # ML engine documentation
│
├── data/                     # Data lake directory (git-ignored data files)
│   ├── raw/                  # Source untouched datasets
│   ├── processed/            # Cleaned, feature-ready datasets
│   ├── artifacts/            # Serialized preprocessors and scalers
│   └── README.md             # Data guidelines & conventions
│
├── tests/                    # Top-level test suite
│   ├── conftest.py           # Global pytest configurations
│   ├── test_project_structure.py # Foundation integrity verification
│   └── README.md
│
├── docker/                   # Deployment & container infrastructure
│   ├── backend/              # Production backend Dockerfile
│   ├── frontend/             # Production frontend Dockerfile (Nginx)
│   └── db/
│       └── init.sql          # PostgreSQL bootstrap initialization
│
├── docs/                     # Technical documentation
│   ├── architecture.md       # Architectural diagrams & specifications
│   ├── api.md                # REST API reference
│   └── development_guide.md  # Detailed setup & developer manual
│
├── .env.example              # Blueprint environment variables
├── .gitignore                # Production git ignore rules
├── docker-compose.yml        # Multi-service local stack
└── README.md                 # Primary project documentation
```

---

## Getting Started & Development Instructions

### 1. Prerequisites
- **Python 3.11+**
- **Node.js 20+**
- **Docker & Docker Compose** (optional)

### 2. Environment Setup
Create your local environment file from the blueprint:
```bash
cp .env.example .env
```

### 3. Backend Development
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\Activate.ps1

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API Base: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### 4. Frontend Development
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

## Running Tests

Run all foundational and backend tests from the project root:
```bash
python -m pytest
```

Run backend unit tests specifically:
```bash
python -m pytest backend/tests
```

---

## Docker Compose Deployment

To launch the full stack (PostgreSQL, FastAPI Backend, React Frontend) in isolated containers:
```bash
docker compose up --build
```

- **Frontend Application**: `http://localhost:5173`
- **Backend API & Swagger**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432`

To shut down:
```bash
docker compose down
```

---

## Security & Best Practices
- **No hardcoded secrets**: All configurations use environment variables via Pydantic Settings.
- **Isolated dependencies**: `backend/`, `ml/`, and `frontend/` have dedicated package managers and manifests.
- **Clean Git footprint**: Sensitive `.env` files, build caches, and datasets are strictly excluded.
