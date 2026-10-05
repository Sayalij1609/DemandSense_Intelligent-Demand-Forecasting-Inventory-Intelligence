# DemandSense Data Lineage & Provenance

This document establishes the end-to-end data lineage from source Kaggle CSV files through transformation and synthetic augmentation to the final canonical dataset.

```
+-------------------------------------------------------------------------------+
|                       RAW KAGGLE SOURCE DATASETS                              |
|   1. retail_store_inventory.csv (SELECTED PRIMARY FOUNDATION)                 |
|   2. customer_shopping_data.csv (INCOMPATIBLE - EXCLUDED)                     |
|   3. online-retail-dataset.csv  (INCOMPATIBLE - EXCLUDED)                     |
|   4. export.csv                 (INCOMPATIBLE - EXCLUDED)                     |
|   5. retail_sales_dataset.csv   (INCOMPATIBLE - EXCLUDED)                     |
|   6. data.csv                   (INCOMPATIBLE - EXCLUDED)                     |
|   7. amazon.csv                 (INCOMPATIBLE - EXCLUDED)                     |
|   8. P & L March 2021.csv       (INCOMPATIBLE - EXCLUDED)                     |
|   9. Sales Dataset.csv          (INCOMPATIBLE - EXCLUDED)                     |
|  10. sales_data.csv             (INCOMPATIBLE - EXCLUDED)                     |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                       REAL-DATA FOUNDATION MAPPING                            |
|  - Date               ───►  date (YYYY-MM-DD)                                 |
|  - Store ID           ───►  store_id (S001 - S005)                            |
|  - Product ID         ───►  product_id (P0001 - P0020)                        |
|  - Category           ───►  category                                          |
|  - Region             ───►  region                                            |
|  - Units Sold         ───►  units_sold (Integer target)                       |
|  - Price              ───►  unit_price ($ Float)                              |
|  - Discount           ───►  discount (Decimal rate: 0.00 - 0.20)              |
|  - Holiday/Promotion  ───►  promotion (Binary marketing flag)                 |
|  - Weather Condition  ───►  weather (Normalized lowercase)                    |
|  - Competitor Pricing ───►  competitor_price ($ Float)                        |
|  - Seasonality        ───►  seasonality                                       |
|  - [Raw Snapshots]    ───►  raw_inventory_level, raw_units_ordered            |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                REPRODUCIBLE SYNTHETIC AUGMENTATION (SEED=42)                  |
|  - Category Lead Times ───►  supplier_lead_time [2-16 days]                   |
|  - Vendor Catalog      ───►  supplier_id [SUPP-GROC-01, ...]                  |
|  - Calendar Lookup     ───►  holiday [US statutory holidays]                  |
|  - Macro Trend Model   ───►  economic_indicator [CPI proxy]                   |
|  - Event Probability   ───►  regional_event [Local surges]                    |
|  - Physical Flow Model ───►  inventory_level (I_t = max(0, I_{t-1} - S + R))  |
|  - Ground Truth Policy ───►  safety_stock, reorder_point, stockout_units      |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
|                    FINAL CANONICAL DATASET (73,100 ROWS)                      |
|            data/processed/demandsense_dataset.parquet (1.19 MB)               |
|            data/processed/demandsense_dataset.csv     (9.12 MB)               |
+-------------------------------------------------------------------------------+
```

---

## Provenance Rules & Guardrails

1. **No Data Fabrication**: Real sales demand (`units_sold`), prices, promotions, and weather are never altered or replaced.
2. **Explicit Labeling**: Every column in the schema is cataloged as `REAL`, `SYNTHETIC`, or `SYNTHETIC_DERIVED` in `data/metadata/synthetic_data_catalog.json` and `data/reports/data_lineage_report.md`.
3. **Audit Trail**: Original raw Kaggle values are preserved side-by-side (`raw_inventory_level`, `raw_units_ordered`, `raw_demand_forecast`) to allow downstream validation and auditability.
4. **Reproducibility**: All synthetic generation processes use a single fixed random seed (`RANDOM_SEED = 42`).
