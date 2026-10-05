# Phase 1: Dataset Analysis & Evaluation Report

**Project**: DemandSense — Intelligent Demand Forecasting & Inventory Intelligence  
**Phase**: Phase 1 — Data Acquisition, Dataset Analysis & Unified Dataset Construction  
**Author**: Data Engineering & ML Architecture Team  
**Date**: October 2026  
**Status**: APPROVED

---

## 1. Executive Summary

During Phase 1, ten raw Kaggle CSV files provided in `data/raw/` were systematically profiled, cataloged, and evaluated against the functional requirements of DemandSense.

The evaluation concluded that **`retail_store_inventory.csv`** is the single ideal primary dataset for DemandSense. It provides a balanced panel of **73,100 records** across **5 stores** and **20 product SKUs** over **731 continuous calendar days** (`2022-01-01` to `2024-01-01`), complete with actual units sold, prices, discounts, promotions, weather, and competitor prices.

The other 9 datasets were determined to be logically incompatible due to divergent timeframes, lack of SKU-level product keys, non-overlapping geographies, or sparse non-daily transaction structures. These 9 datasets are preserved in `data/raw/kaggle/` and documented in the dataset catalog, but excluded from integration to prevent invalid or misleading joins.

To meet the complete DemandSense target schema for inventory decision intelligence, missing business dimensions (**supplier lead time**, **demand-coupled inventory flow**, and **calendar holiday indicators**) are generated using rigorous, deterministic, reproducible algorithms (`RANDOM_SEED = 42`) without modifying or replacing any real Kaggle sales data.

---

## 2. Inventory of Evaluated Datasets

| Dataset Filename | Size | Rows | Columns | Timeframe | Granularity | Business Classification | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`retail_store_inventory.csv`** | **6.19 MB** | **73,100** | **15** | **2022-01-01 to 2024-01-01** | **Daily Store-SKU** | **Retail Sales & Inventory** | **SELECTED (Primary Foundation)** |
| `customer_shopping_data.csv` | 7.54 MB | 99,457 | 10 | 2021-01-01 to 2023-03-08 | Transaction / Mall | Mall Invoices | Incompatible (No SKU IDs; Istanbul Malls) |
| `online-retail-dataset.csv` | 45.04 MB | 541,909 | 8 | 2010-12-01 to 2011-12-09 | Transaction Line | E-Commerce Wholesale | Incompatible (2010-2011 UK gifts; no stores) |
| `export.csv` | 28.43 MB | 341,037 | 9 | 2020-06 to 2020-09 (4 mos) | Monthly Item | Wholesale Liquor Transfers | Incompatible (Monthly wholesale liquor) |
| `retail_sales_dataset.csv` | 676 KB | 4,310 | 21 | 2020-01-01 to 2024-12-30 | Transaction / Order | Customer Purchases | Incompatible (Sparse nationwide transactions) |
| `data.csv` | 1.25 MB | 5,000 | 24 | 2013-01-05 to 2017-10-01 | Order Line | B2B Commercial Equipment | Incompatible (2013-2017 Australian B2B) |
| `amazon.csv` | 4.74 MB | 1,465 | 16 | Static snapshot | Product Catalog | E-Commerce Reviews | Incompatible (Catalog only, no time series) |
| `P  L March 2021.csv` | 136 KB | 1,330 | 18 | March 2021 | SKU Snapshot | Marketplace Pricing Matrix | Incompatible (Apparel MRP matrix, no dates) |
| `Sales Dataset.csv` | 118 KB | 1,194 | 12 | 2020-03-22 to 2025-03-15 | Order | Consumer Orders | Incompatible (Sparse sub-category orders) |
| `sales_data.csv` | 105 KB | 1,000 | 14 | 2023-01-01 to 2024-01-01 | Transaction | Sales Rep Orders | Incompatible (Sparse sales rep records) |

---

## 3. Deep Dive: Why `retail_store_inventory.csv` Was Selected

### 3.1 Structural Panel Balance
- **Temporal Span**: Exactly 731 days (2 full years, 365 days in 2022 + 365 days in 2023 + 1 day on 2024-01-01).
- **Physical Stores**: Exactly 5 stores (`S001`, `S002`, `S003`, `S004`, `S005`).
- **Product SKUs**: Exactly 20 products (`P0001` through `P0020`), evenly distributed across 5 categories (4 SKUs per category).
- **Time-Series Completeness**: Every (Store, Product) pair has **exactly 731 records**. Zero missing days, zero duplicate timestamps, and zero missing values across all 15 columns.

### 3.2 Richness of Business Features
The dataset contains real, observed data for:
- Historical demand (`Units Sold`, range: 1 to 498 units/day)
- Pricing and promotions (`Price`, `Discount` at 0%, 5%, 10%, 15%, 20%, and `Holiday/Promotion` flag)
- Exogenous environmental signals (`Weather Condition`: Rainy, Sunny, Cloudy, Snowy; `Seasonality`: Spring, Summer, Autumn, Winter)
- Competitive intelligence (`Competitor Pricing`)

### 3.3 Empirical Discovery on Raw Inventory Level
Empirical testing revealed that while the Kaggle dataset includes an `Inventory Level` column, it was generated independently of demand and does not obey physical inventory conservation ($I_t = I_{t-1} - S_t + R_t$). Specifically, inventory levels jump arbitrarily regardless of previous stock, sales, or replenishment arrivals.

**Engineering Decision**:
1. Preserve the raw Kaggle inventory value in `raw_inventory_level` for auditing.
2. Simulate a demand-coupled, physically consistent `inventory_level` using real units sold, realistic lead times, and replenishment orders. This enables genuine stockout risk, overstock risk, and safety stock evaluation.

---

## 4. Incompatibility Analysis of Excluded Datasets

Attempting to join the other 9 datasets into `retail_store_inventory.csv` would violate data engineering principles:
1. **Identifier Mismatch**: None of the 9 files contain product IDs matching `P0001`–`P0020` or store IDs matching `S001`–`S005`.
2. **Temporal Discordance**: `online-retail-dataset.csv` (2010–2011) and `data.csv` (2013–2017) do not overlap with 2022–2024.
3. **Granularity Discordance**: `export.csv` is monthly wholesale alcohol distribution, while `customer_shopping_data.csv` contains transactional invoices without product-level SKUs.
4. **Conclusion**: Forcing joins through artificial key-mapping would introduce fake relationships and corrupt the integrity of the forecasting models.

---

## 5. Next Steps for Phase 1 Execution

1. Implement `ml/data_generation/` modules for reproducible, physically realistic synthetic supporting dimensions (`supplier_lead_time`, `inventory_level`, `holiday`).
2. Implement `ml/data_pipeline/` modules automating profiling, schema mapping, transformation, integration, and validation.
3. Generate the unified dataset in `data/processed/demandsense_dataset.parquet` and `data/processed/demandsense_dataset.csv`.
4. Validate data quality and generate lineage reports.
