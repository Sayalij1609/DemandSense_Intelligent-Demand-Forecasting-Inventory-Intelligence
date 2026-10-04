# DemandSense System Architecture

DemandSense is an end-to-end intelligent demand forecasting and inventory optimization system built for production operations.

```
+-----------------------------------------------------------------------------------+
|                                  USER / CLIENT                                    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        React + Vite + Tailwind Frontend                           |
|       - Demand Forecast Dashboard          - Uncertainty Bands Visualizer         |
|       - Inventory Health Overview          - Stockout / Overstock Alert Panel     |
+-----------------------------------------------------------------------------------+
                                         │  HTTP / REST
                                         ▼
+-----------------------------------------------------------------------------------+
|                                FastAPI Backend                                    |
|   - API v1 Routing                         - Request Validation (Pydantic v2)     |
|   - Business Services Layer                - SQLAlchemy Session & Query Engine    |
+-----------------------------------------------------------------------------------+
             │                                                  │
             ▼                                                  ▼
+-------------------------+                       +---------------------------------+
|   PostgreSQL Database   |                       |    DemandSense ML Engine        |
|  - Historical Sales     |                       |  - Feature Engineering (Lags)   |
|  - Inventory Metadata   |                       |  - Traditional ML (LightGBM/XGB)|
|  - Forecast Snapshots   |                       |  - Deep Learning (PyTorch)      |
|  - Order Recommendations|                       |  - Probabilistic Uncertainty    |
+-------------------------+                       |  - Inventory Intelligence Engine|
                                                  +---------------------------------+
```

## Core Modules

### 1. Data Collection & Preprocessing (`ml/data/`, `data/`)
- Ingestion of point-of-sale time series, promotions, prices, and stock counts.
- Missing value imputation, calendar alignments, and outlier mitigation.

### 2. Time-Series Feature Engineering (`ml/features/`)
- Lagged demand variables (t-1, t-7, t-14, t-28, t-365).
- Rolling summary statistics (mean, std, min, max, exponentially weighted averages).
- Cyclical calendar features (day of week, month, holidays, quarter).

### 3. Forecasting Engines (`ml/models/`)
- **Traditional ML**: Ridge regression, Random Forest, LightGBM, and XGBoost.
- **Deep Learning**: Sequence modeling using PyTorch (LSTM, Temporal Attention).
- **Hybrid Ensembles**: Weighted aggregation for optimal generalized accuracy.

### 4. Inventory Intelligence (`ml/inventory/`)
Translates forecasted demand distributions into actionable operational decisions:
- **Expected Demand**: Projected quantity over lead time.
- **Demand Trend**: Directional indicators (rising, stable, declining).
- **Forecast Uncertainty**: Probabilistic intervals (p10, p50, p90).
- **Safety Stock**: Service level-adjusted buffer inventory calculation.
- **Reorder Point (ROP)**: Dynamic threshold triggering new procurement orders.
- **Stockout & Overstock Risks**: Quantified probability percentages.
- **Recommended Order Quantity (ROQ)**: Economic order calculation minimizing holding and shortage costs.

### 5. API Backend (`backend/`)
- Clean modular FastAPI architecture.
- Pydantic v2 schemas for robust serialization.
- Asynchronous endpoints with PostgreSQL connectivity via SQLAlchemy.

### 6. Interactive Frontend (`frontend/`)
- Modern React SPA powered by Vite.
- Tailwind CSS styling for a crisp, responsive, dark/light modern UI.
- Interactive Recharts charts for time-series demand projections and uncertainty bands.
