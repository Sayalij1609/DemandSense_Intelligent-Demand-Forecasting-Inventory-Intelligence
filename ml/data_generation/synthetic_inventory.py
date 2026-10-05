"""Physical inventory flow simulation module.

Simulates a continuous, demand-coupled replenishment inventory lifecycle
adhering to fundamental conservation of physical inventory:
I_t = max(0, I_{t-1} - Units_Sold_t + Replenishment_Arrived_t).
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def simulate_single_series_inventory(
    group: pd.DataFrame,
    service_level_z: float = 1.645,
) -> pd.DataFrame:
    """Simulate inventory dynamics for a single (Store, Product) time series.

    Args:
        group: Sorted chronological dataframe for one store-product pair.
        service_level_z: Z-score for service level (1.645 corresponds to 95%).

    Returns:
        Dataframe augmented with 'inventory_level', 'safety_stock', 'reorder_point',
        'replenishment_received', and 'stockout_units'.
    """
    n_days = len(group)
    units_sold = group["units_sold"].values
    lead_times = group["supplier_lead_time"].values

    # 1. Compute time-series demand baseline statistics
    mean_demand = max(float(np.mean(units_sold)), 1.0)
    std_demand = max(float(np.std(units_sold)), 1.0)
    avg_lead_time = max(float(np.mean(lead_times)), 1.0)

    # 2. Compute Ground-Truth Policy Benchmarks
    # Safety Stock: SS = Z * sqrt(L * sigma_d^2)
    safety_stock = int(np.ceil(service_level_z * np.sqrt(avg_lead_time * (std_demand ** 2))))
    safety_stock = max(safety_stock, 10)

    # Reorder Point: ROP = L * mu_d + SS
    reorder_point = int(np.ceil((avg_lead_time * mean_demand) + safety_stock))

    # Economic / Standard Order Quantity: Q
    order_quantity = int(np.ceil(max(1.8 * avg_lead_time * mean_demand, 40)))

    # Initial inventory at t=0
    initial_inventory = int(safety_stock + (1.2 * avg_lead_time * mean_demand))

    # 3. Simulate day-by-day transitions
    inv_levels = np.zeros(n_days, dtype=int)
    replenish_received = np.zeros(n_days, dtype=int)
    stockout_units = np.zeros(n_days, dtype=int)

    # Queue of in-transit orders: [(delivery_day, quantity)]
    pipeline_orders: List[Tuple[int, int]] = []

    current_inv = initial_inventory

    for t in range(n_days):
        # A. Arrive in-transit orders due on day t
        arrived = 0
        remaining_pipeline = []
        for delivery_day, qty in pipeline_orders:
            if delivery_day == t:
                arrived += qty
            elif delivery_day > t:
                remaining_pipeline.append((delivery_day, qty))
        pipeline_orders = remaining_pipeline

        replenish_received[t] = arrived
        available_inv = current_inv + arrived

        # B. Customer demand fulfillment
        demand = units_sold[t]
        if demand <= available_inv:
            ending_inv = available_inv - demand
            stockout = 0
        else:
            ending_inv = 0
            stockout = demand - available_inv

        inv_levels[t] = ending_inv
        stockout_units[t] = stockout
        current_inv = ending_inv

        # C. Evaluate inventory position and trigger order if at/below ROP
        pipeline_qty = sum(qty for _, qty in pipeline_orders)
        inventory_position = current_inv + pipeline_qty

        if inventory_position <= reorder_point:
            delivery_day = t + int(lead_times[t])
            pipeline_orders.append((delivery_day, order_quantity))

    res = group.copy()
    res["inventory_level"] = inv_levels
    res["safety_stock"] = safety_stock
    res["reorder_point"] = reorder_point
    res["replenishment_received"] = replenish_received
    res["stockout_units"] = stockout_units
    return res


def simulate_inventory_flow(df: pd.DataFrame, random_seed: int = 42) -> pd.DataFrame:
    """Execute inventory simulation across all store-product series in the dataset.

    Args:
        df: Input dataframe sorted by store_id, product_id, date.
        random_seed: Random seed for reproducibility.

    Returns:
        Consolidated dataframe with physically consistent inventory fields.
    """
    df = df.sort_values(["store_id", "product_id", "date"]).reset_index(drop=True)

    series_dfs = []
    for (store, prod), group in df.groupby(["store_id", "product_id"], sort=False):
        simulated = simulate_single_series_inventory(group)
        series_dfs.append(simulated)

    result_df = pd.concat(series_dfs, ignore_index=True)
    # Restore chronological sort
    result_df = result_df.sort_values(["date", "store_id", "product_id"]).reset_index(drop=True)
    return result_df
