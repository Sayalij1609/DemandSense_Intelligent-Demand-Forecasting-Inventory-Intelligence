# DemandSense Synthetic Data Methodology

This document outlines the mathematical and operational principles governing synthetic data generation in DemandSense.

---

## 1. Grounding Principles

Synthetic data generation in DemandSense strictly adheres to the following constraints:
1. **Never Replace Real Sales**: Actual customer demand (`units_sold`), prices, discounts, promotions, and weather from Kaggle are 100% preserved.
2. **Domain-Coupled, Never Independent**: Generated values are physically and statistically coupled to the real data (e.g. inventory decreases as sales occur; lead times depend on product category).
3. **100% Reproducibility**: All random processes are seeded with `RANDOM_SEED = 42`.
4. **Full Traceability**: All generated attributes are cataloged in `data/metadata/synthetic_data_catalog.json` and documented in data lineage reports.

---

## 2. Supplier Lead-Time Modeling

Supply chains exhibit category-dependent lead times driven by physical logistics:
- **Groceries**: Highly perishable, localized sourcing $\rightarrow$ Base: 3 days, bounded $[2, 5]$ days.
- **Clothing**: Regional apparel warehouses $\rightarrow$ Base: 5 days, bounded $[4, 8]$ days.
- **Toys**: Regional wholesale distributors $\rightarrow$ Base: 7 days, bounded $[5, 10]$ days.
- **Electronics**: High-value technology distributors $\rightarrow$ Base: 9 days, bounded $[7, 13]$ days.
- **Furniture**: Bulky freight carriers $\rightarrow$ Base: 14 days, bounded $[10, 18]$ days.

### Perturbation Function
$$L_{t} = \text{clip}\left( L_{\text{base}} + \Delta_{\text{weather}} + \Delta_{\text{holiday}},\; L_{\min},\; L_{\max} \right)$$
- Severe weather (`Snowy`): $\Delta_{\text{weather}} = +1$ with $P = 0.70$.
- Promotional surges (`promotion = 1`): $\Delta_{\text{holiday}} = +1$ with $P = 0.50$.

---

## 3. Physical Inventory Flow Simulation

Empirical testing revealed that raw Kaggle `Inventory Level` was generated independently and violated physical inventory balance ($I_t \ne I_{t-1} - S_t + R_t$). To support legitimate stockout risk and safety stock evaluation, we simulate true physical inventory dynamics.

### System Equations
For each (Store, Product) series in chronological order:

1. **Baseline Metrics**:
   - Mean daily demand: $\mu_d = \frac{1}{N} \sum_{t=1}^N S_t$
   - Standard deviation of demand: $\sigma_d = \sqrt{\frac{1}{N-1} \sum_{t=1}^N (S_t - \mu_d)^2}$
   - Average lead time: $\bar{L}$

2. **Policy Thresholds (95% Cycle Service Level, $Z = 1.645$)**:
   - Safety Stock: $SS = \left\lceil Z \cdot \sqrt{\bar{L} \cdot \sigma_d^2} \right\rceil$
   - Reorder Point: $ROP = \left\lceil \bar{L} \cdot \mu_d + SS \right\rceil$
   - Batch Order Quantity: $Q = \left\lceil \max(1.8 \cdot \bar{L} \cdot \mu_d,\; 40) \right\rceil$

3. **Daily Inventory State Transition**:
   $$I_t^{\text{avail}} = I_{t-1} + R_t$$
   $$I_t = \max\left(0,\; I_t^{\text{avail}} - S_t\right)$$
   $$\text{Stockout Units}_t = \max\left(0,\; S_t - I_t^{\text{avail}}\right)$$

4. **Replenishment Trigger**:
   - Inventory position: $IP_t = I_t + \sum \text{Orders in Pipeline}$
   - If $IP_t \le ROP$: Dispatch order of size $Q$ scheduled to arrive on day $t + L_t$.

This guarantees that:
- Inventory strictly decreases when goods are sold.
- Inventory never drops below 0.
- Replenishment arrives with realistic lead-time delays.
- Stockouts occur under realistic demand spikes.

---

## 4. Calendar Holidays & Economic Indices

- **Calendar Holidays**: Mapped deterministically against statutory US Federal holidays (New Year's, Memorial Day, July 4, Labor Day, Thanksgiving, Christmas, etc.).
- **Economic Index**: Modeled after the 2022–2023 headline CPI trajectory (281.0 to 307.0) to serve as a non-stationary macro covariate for deep learning models.
