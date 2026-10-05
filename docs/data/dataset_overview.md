# DemandSense Dataset Overview

**Project**: DemandSense — Intelligent Demand Forecasting & Inventory Intelligence  
**Phase**: Phase 1: Data Acquisition & Unified Construction  
**Status**: Production-Ready  
**Canonical Output**:
- Primary: `data/processed/demandsense_dataset.parquet`
- Fallback: `data/processed/demandsense_dataset.csv`

---

## 1. Executive Summary

DemandSense requires a high-resolution, unbroken time-series panel that pairs historical product demand with pricing, promotional campaigns, inventory state transitions, and supplier replenishment dynamics. 

Following a rigorous evaluation of ten provided Kaggle CSV files, **`retail_store_inventory.csv`** was identified as the only dataset satisfying all operational criteria. It provides **73,100 observations** across **5 physical stores** and **20 product SKUs** over **731 continuous calendar days** (January 1, 2022 to January 1, 2024).

The remaining nine Kaggle datasets represent non-overlapping retail domains, transactional e-commerce gift logs from 2010–2011, county liquor wholesale distribution, or sparse non-daily customer logs that lack SKU-level identifiers. They are cataloged in `data/metadata/dataset_catalog.json` and preserved unchanged in `data/raw/kaggle/`.

---

## 2. Dataset Key Metrics

| Dimension | Specification |
| :--- | :--- |
| **Observation Horizon** | 2022-01-01 to 2024-01-01 (731 continuous days) |
| **Panel Granularity** | Daily Store-SKU level (`date` + `store_id` + `product_id`) |
| **Total Rows** | Exactly **73,100 records** (731 days x 5 stores x 20 products) |
| **Total Columns** | **25 attributes** (11 canonical core + 14 auxiliary and audit features) |
| **Product SKUs** | **20 unique items** (`P0001` through `P0020`), 4 per category |
| **Product Categories** | **5 departments**: Groceries, Clothing, Toys, Electronics, Furniture |
| **Physical Stores** | **5 locations**: `S001`, `S002`, `S003`, `S004`, `S005` |
| **Geographic Regions** | **4 territories**: North, South, East, West |
| **Real Kaggle Attributes** | 60% (Historical sales, prices, discounts, promotions, weather, competitor prices) |
| **Synthetic Supporting Dimensions** | 40% (Supplier lead time, coupled inventory level, calendar holidays, safety stocks) |

---

## 3. Downstream Machine Learning Readiness

The unified dataset directly supports all downstream DemandSense objectives:

1. **Multivariate Time-Series Forecasting**: Unbroken daily sequence suitable for rolling-window feature engineering (lags, EWMA, rolling standard deviation) without imputation.
2. **Deep Learning Sequence Modeling**: Perfectly balanced 100 series (5 stores x 20 SKUs x 731 timesteps) ready for PyTorch 3D tensor extraction `[batch_size, sequence_length, features]`.
3. **Inventory Decision Intelligence**: Physically consistent on-hand inventory levels enable ground-truth benchmark evaluation for:
   - Dynamic safety stock calculation
   - Reorder point (ROP) calculation
   - Stockout risk quantification
   - Overstock carrying cost minimization
   - Recommended order quantity (ROQ)
