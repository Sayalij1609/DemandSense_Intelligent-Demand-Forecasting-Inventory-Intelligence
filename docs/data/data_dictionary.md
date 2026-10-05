# DemandSense Data Dictionary

This data dictionary defines all 25 columns present in `data/processed/demandsense_dataset.parquet`.

---

## 1. Core Target Schema (11 Columns)

| Column Name | Data Type | Null Count (%) | Real / Synthetic | Business Description & Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `date` | `string (YYYY-MM-DD)` | 0 (0.0%) | **REAL** | Calendar observation date (`2022-01-01` to `2024-01-01`). |
| `product_id` | `string` | 0 (0.0%) | **REAL** | SKU identifier (`P0001` - `P0020`). |
| `store_id` | `string` | 0 (0.0%) | **REAL** | Retail store identifier (`S001` - `S005`). |
| `category` | `string` | 0 (0.0%) | **REAL** | Merchandise category: `Groceries`, `Toys`, `Electronics`, `Furniture`, `Clothing`. |
| `units_sold` | `int64` | 0 (0.0%) | **REAL** | **Primary demand target**. Daily units purchased by customers (Range: 1 to 498). |
| `unit_price` | `float64` | 0 (0.0%) | **REAL** | Unit retail selling price in USD (Range: $15.00 to $120.00). |
| `discount` | `float64` | 0 (0.0%) | **REAL** | Promotional discount rate (Values: 0.00, 0.05, 0.10, 0.15, 0.20). |
| `promotion` | `int64` | 0 (0.0%) | **REAL** | Binary marketing campaign indicator (1 = Active promotional campaign, 0 = Standard). |
| `holiday` | `int64` | 0 (0.0%) | **SYNTHETIC_DERIVED** | Binary indicator for official national statutory holidays (US Federal calendar). |
| `inventory_level` | `int64` | 0 (0.0%) | **SYNTHETIC** | On-hand physical inventory at end of day, obeying $I_t = \max(0, I_{t-1} - S_t + R_t)$. |
| `supplier_lead_time`| `int64` | 0 (0.0%) | **SYNTHETIC** | Days required for supplier replenishment to arrive at the store (Range: 2 to 16 days). |

---

## 2. Contextual & Exogenous Features (6 Columns)

| Column Name | Data Type | Real / Synthetic | Business Description |
| :--- | :--- | :--- | :--- |
| `weather` | `string` | **REAL** | Local ambient weather condition: `sunny`, `rainy`, `cloudy`, `snowy`. |
| `competitor_price`| `float64` | **REAL** | Local competitor market price for comparable product ($). |
| `economic_indicator`| `float64` | **SYNTHETIC** | Macroeconomic headline Consumer Price Index (CPI) proxy trend (281.0 to 307.0). |
| `regional_event` | `int64` | **SYNTHETIC** | Binary flag (0/1) for regional festivals, fairs, or weekend shopping surges. |
| `region` | `string` | **REAL** | Store geographic territory: `North`, `South`, `East`, `West`. |
| `seasonality` | `string` | **REAL** | Astronomical seasonal phase: `Spring`, `Summer`, `Autumn`, `Winter`. |

---

## 3. Supply Chain Benchmarks & Simulation Auditing (8 Columns)

| Column Name | Data Type | Real / Synthetic | Business Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | `string` | **SYNTHETIC** | Assigned primary vendor identifier (`SUPP-GROC-01`, etc.). |
| `safety_stock` | `int64` | **SYNTHETIC_DERIVED** | Calculated 95% service-level buffer stock threshold ($SS = Z \cdot \sqrt{L \cdot \sigma_d^2}$). |
| `reorder_point` | `int64` | **SYNTHETIC_DERIVED** | Dynamic inventory threshold triggering replenishment ($ROP = L \cdot \mu_d + SS$). |
| `stockout_units`| `int64` | **SYNTHETIC_DERIVED** | Unfulfilled daily customer demand due to stock exhaustion ($\max(0, Demand - Inv)$). |
| `replenishment_received` | `int64`| **SYNTHETIC_DERIVED** | Number of units delivered by supplier on that date. |
| `raw_inventory_level` | `int64` | **REAL** | Raw, uncoupled inventory snapshot preserved from Kaggle source. |
| `raw_units_ordered` | `int64` | **REAL** | Raw units ordered preserved from Kaggle source. |
| `raw_demand_forecast` | `float64` | **REAL** | Baseline statistical forecast provided in raw Kaggle dataset. |
