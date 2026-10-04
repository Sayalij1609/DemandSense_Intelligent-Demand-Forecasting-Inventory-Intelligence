# DemandSense Machine Learning Engine

This directory houses the forecasting and inventory decision intelligence algorithms for DemandSense.

## Modular Architecture

- **`data/`**: Ingestion connectors, raw data transformations, and dataset loaders.
- **`features/`**: Time-series feature engineering (calendar signals, rolling statistics, lag features, price elasticity indicators).
- **`models/`**: Forecasting algorithms:
  - Traditional ML: Ridge/Lasso, Random Forest, LightGBM, XGBoost.
  - Deep Learning: LSTM/GRU, Temporal Fusion Transformers / N-BEATS with PyTorch.
  - Ensembles: Stacking and weighted hybrid forecasting.
- **`evaluation/`**: Time-series cross-validation (rolling window, expanding window), error metrics (MAE, RMSE, WAPE, SMAPE), and benchmarking tables.
- **`inventory/`**: Translates probabilistic demand forecasts into inventory actions:
  - Expected demand & trend analysis
  - Forecast uncertainty estimation (prediction intervals)
  - Safety stock calculation (service-level based)
  - Reorder point (ROP) calculation
  - Stockout & overstock risk quantification
  - Recommended order quantity (ROQ)
- **`pipelines/`**: Reproducible orchestration for training, model selection, serialization, and batch/real-time inference.

## Dependency Management

ML dependencies are managed independently in `requirements.txt`:
```bash
pip install -r ml/requirements.txt
```
