# DemandSense Final Dataset Quality Report

**Generated**: October 2026  
**Pipeline Run**: Phase 1 Unified Construction  
**Status**: **PASSED ALL 15 QUALITY ASSERTIONS**

---

## 1. Core Dataset Dimensions

| Metric | Value | Description |
| :--- | :--- | :--- |
| **Total Rows** | **73,100** | Fully balanced daily store-product panel |
| **Total Columns** | **25** | Complete canonical and auxiliary features |
| **Date Range** | **2022-01-01 to 2024-01-01** | Exactly 2 full calendar years |
| **Total Calendar Days** | **731 days** | Continuous unbroken time series |
| **Unique Stores** | **5** | S001 through S005 |
| **Unique Products** | **20** | P0001 through P0020 (4 SKUs per category) |
| **Unique Categories** | **5** | Groceries, Toys, Electronics, Furniture, Clothing |
| **Duplicate Business Keys** | **0** | Zero duplicates on (date, store_id, product_id) |
| **Missing Values in Core Columns** | **0 (0.0%)** | Zero nulls in core attributes |

---

## 2. Real vs. Synthetic Feature Composition

- **Real Kaggle Columns**: **60.0%** (Historical units sold, unit prices, discounts, promotion flags, weather condition, competitor prices, region, seasonality, raw benchmark forecast).
- **Synthetic Supporting Columns**: **40.0%** (Supplier lead time, physically coupled inventory level, calendar holidays, safety stock, reorder point, economic index, regional events).
- **Random Seed**: Fixed at `RANDOM_SEED = 42` for 100% mathematical reproducibility.

---

## 3. Key Distribution Summaries

### 3.1 Units Sold (Demand Target)
- **Mean Daily Sales**: 136.46 units/day
- **Standard Deviation**: 108.92
- **Min / Max**: 0 / 499 units
- **25% / 50% / 75%**: 49 / 107 / 203 units

### 3.2 Inventory Level (Physically Coupled On-Hand Stock)
- **Mean On-Hand Stock**: 1515.76 units
- **Min / Max**: 0 / 3742 units
- **Physical Conservation**: Obeyed at 100% across all 100 individual time series.

### 3.3 Supplier Lead Time
- **Mean Lead Time**: 8.03 days
- **Min / Max**: 3 / 16 days
- **Category Grounding**: Bounded by product classification (Groceries: 2-5d, Furniture: 10-18d).

---

## 4. Dataset Limitations & Operational Context
1. **Catalog Size**: 20 product SKUs across 5 categories provides a focused, high-integrity benchmark panel.
2. **Geographic Scope**: 5 store locations across 4 major regions (North, South, East, West).
3. **Inventory Simulation**: While derived from real demand and order cycles, inventory levels represent a simulated physical flow rather than an audited warehouse ledger.
