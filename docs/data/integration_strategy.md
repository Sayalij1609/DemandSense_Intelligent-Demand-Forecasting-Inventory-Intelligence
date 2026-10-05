# DemandSense Data Integration Strategy

This document explains the technical and business rationale governing dataset inclusion, join compatibility, and the exclusion of non-integrable Kaggle CSV files.

---

## 1. Integration Principles

The DemandSense architecture adheres to four core data integration tenets:

1. **Entities Must Align**: Datasets can only be merged if they share unambiguous, identical real-world entities (e.g. matching SKU identifiers and matching physical store IDs).
2. **Granularity Must Match**: Daily time series cannot be joined with monthly aggregates or sporadic single-transaction logs without introducing artificial distortion or data leakage.
3. **Temporal Alignment**: Records must share an overlapping calendar horizon.
4. **No Artificial Joins**: Two datasets must never be forcibly merged simply because they share column names (e.g. `product_id` or `price`) when the underlying values belong to unrelated namespaces.

---

## 2. Incompatibility Matrix

| Evaluated CSV | Common Keys with Primary | Date Overlap | Decision | Technical Rationale |
| :--- | :--- | :--- | :--- | :--- |
| `customer_shopping_data.csv` | Category names only | Partial (2021-2023) | **EXCLUDED** | Lacks product SKU IDs (only 8 categories); store entities are Turkish shopping malls. Merging would destroy SKU-level resolution. |
| `online-retail-dataset.csv` | None | None (2010-2011) | **EXCLUDED** | 10-year temporal gap; UK e-commerce giftware with StockCodes (`85123A`); non-store structure. |
| `export.csv` | None | None (2020 only) | **EXCLUDED** | Monthly wholesale liquor distribution in Montgomery County; incompatible granularity and domain. |
| `retail_sales_dataset.csv` | Category names only | Partial (2020-2024) | **EXCLUDED** | Highly sparse order transactions (4,310 rows across 4 years nationally); lacks store IDs. |
| `data.csv` | None | None (2013-2017) | **EXCLUDED** | 5-year temporal gap; Australian commercial B2B office equipment. |
| `amazon.csv` | None | None (Static) | **EXCLUDED** | Review catalog with Amazon ASINs; no temporal demand or store locations. |
| `P  L March 2021.csv` | None | None (March 2021) | **EXCLUDED** | Static apparel MRP matrix; no time series. |
| `Sales Dataset.csv` | None | Partial (2020-2025) | **EXCLUDED** | Sparse orders without SKU IDs or store identifiers. |
| `sales_data.csv` | None | Partial (2023) | **EXCLUDED** | Sparse sales rep transactions (only 1,000 orders across 100 products). |

---

## 3. Real-Data Foundation Strategy

Because `retail_store_inventory.csv` already represents a cohesive, balanced, daily multi-store and multi-product panel, it serves as the **sole real-data foundation**.

Rather than introducing noisy, fabricated joins from unrelated files, the pipeline extracts 100% of real historical demand, pricing, discounts, promotions, weather, and competitor prices from `retail_store_inventory.csv`, and uses rigorous domain simulations for the missing supply chain parameters.
