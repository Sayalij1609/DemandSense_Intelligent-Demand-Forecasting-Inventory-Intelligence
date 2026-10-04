# DemandSense Data Directory

This directory stores datasets utilized for training, validation, and offline benchmarking.

## Subdirectories

- **`raw/`**: Unmodified source datasets (e.g., CSV, Parquet, JSON files). Kept immutable for reproducibility.
- **`processed/`**: Cleaned, imputed, aggregated, and feature-engineered datasets ready for model consumption.
- **`artifacts/`**: Serialized intermediate artifacts, such as scalers, category encoders, and dataset splits.

> **Note:** Data files are excluded from Git tracking via `.gitignore` to prevent repository bloat and data leakage.
