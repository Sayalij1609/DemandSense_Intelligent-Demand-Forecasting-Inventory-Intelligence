# DemandSense Data Lineage & Provenance Report

**Generated**: October 2026  
**Source**: Kaggle `retail_store_inventory.csv` + Reproducible Synthetic Augmentations (`RANDOM_SEED = 42`)  

This report provides field-level traceability distinguishing real Kaggle observations from synthetic supporting dimensions.

| Final Column | Source Dataset | Original Column | Type | Transformation | Generation Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | `retail_store_inventory.csv` | `Date` | **REAL** | ISO-8601 date parse (YYYY-MM-DD) | None (Real Kaggle data) |
| `product_id` | `retail_store_inventory.csv` | `Product ID` | **REAL** | Strip whitespace | None (Real Kaggle data) |
| `store_id` | `retail_store_inventory.csv` | `Store ID` | **REAL** | Strip whitespace | None (Real Kaggle data) |
| `category` | `retail_store_inventory.csv` | `Category` | **REAL** | Direct mapping | None (Real Kaggle data) |
| `units_sold` | `retail_store_inventory.csv` | `Units Sold` | **REAL** | Cast to int64 | None (Real Kaggle data) |
| `unit_price` | `retail_store_inventory.csv` | `Price` | **REAL** | Round to 2 decimal places | None (Real Kaggle data) |
| `discount` | `retail_store_inventory.csv` | `Discount` | **REAL** | Percentage / 100.0 (rate 0.0 to 0.20) | None (Real Kaggle data) |
| `promotion` | `retail_store_inventory.csv` | `Holiday/Promotion` | **REAL** | Binary flag (0/1) | None (Real Kaggle data) |
| `holiday` | `calendar_generator` | `N/A` | **SYNTHETIC_DERIVED** | Deterministic US federal holiday calendar mapping | National statutory holiday lookup (2022-2024) |
| `inventory_level` | `inventory_flow_simulation` | `N/A` | **SYNTHETIC** | Dynamic inventory conservation simulation: I_t = max(0, I_{t-1} - S_t + R_t) | Continuous replenishment inventory flow with ROP & lead-time delays |
| `supplier_lead_time` | `supplier_catalog_assignment` | `N/A` | **SYNTHETIC** | Category-grounded base assignment with weather/holiday perturbations | Category baseline lead time [2-16 days] + logistics perturbation |
| `weather` | `retail_store_inventory.csv` | `Weather Condition` | **REAL** | Lowercase string normalization | None (Real Kaggle data) |
| `competitor_price` | `retail_store_inventory.csv` | `Competitor Pricing` | **REAL** | Round to 2 decimal places | None (Real Kaggle data) |
| `economic_indicator` | `macro_economic_proxy` | `N/A` | **SYNTHETIC** | 2022-2023 US CPI inflation index trajectory | Historical macroeconomic headline CPI proxy |
| `regional_event` | `regional_event_generator` | `N/A` | **SYNTHETIC** | Weekend/seasonal probability sampling | Regional expo/festival indicator (seed 42) |
| `region` | `retail_store_inventory.csv` | `Region` | **REAL** | Direct mapping | None (Real Kaggle data) |
| `seasonality` | `retail_store_inventory.csv` | `Seasonality` | **REAL** | Direct mapping | None (Real Kaggle data) |
| `supplier_id` | `supplier_catalog_assignment` | `N/A` | **SYNTHETIC** | Category-to-vendor mapping | Deterministic vendor ID assignment |
| `safety_stock` | `inventory_flow_simulation` | `N/A` | **SYNTHETIC_DERIVED** | SS = Z * sqrt(L * sigma_d^2) | 95% service level buffer stock calculation |
| `reorder_point` | `inventory_flow_simulation` | `N/A` | **SYNTHETIC_DERIVED** | ROP = L * mu_d + SS | Lead-time demand + buffer stock replenishment trigger |
| `stockout_units` | `inventory_flow_simulation` | `N/A` | **SYNTHETIC_DERIVED** | max(0, Demand - Available_Inv) | Recorded unfulfilled customer demand |
| `replenishment_received` | `inventory_flow_simulation` | `N/A` | **SYNTHETIC_DERIVED** | In-transit arrival tracking | Delivered purchase order volume |
| `raw_inventory_level` | `retail_store_inventory.csv` | `Inventory Level` | **REAL** | Direct preservation of raw Kaggle value | None (Real Kaggle data) |
| `raw_units_ordered` | `retail_store_inventory.csv` | `Units Ordered` | **REAL** | Direct preservation of raw Kaggle value | None (Real Kaggle data) |
| `raw_demand_forecast` | `retail_store_inventory.csv` | `Demand Forecast` | **REAL** | Direct preservation of raw Kaggle value | None (Real Kaggle data) |

---

## Real Data Integrity Guarantees
- **Zero Alterations to Historical Sales**: All `units_sold` values match raw Kaggle numbers exactly.
- **Preserved Pricing & Discounts**: Real `Price`, `Discount`, and `Competitor Pricing` are preserved directly.
- **Preserved Environmental Factors**: Real `Weather Condition` and `Seasonality` are preserved intact.
- **Auditable Raw Artifacts**: The raw Kaggle inventory snapshots (`raw_inventory_level`), ordered units (`raw_units_ordered`), and baseline forecast (`raw_demand_forecast`) are retained in the dataset for side-by-side auditability.