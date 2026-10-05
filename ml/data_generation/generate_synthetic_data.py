"""Master synthetic data generation orchestrator.

Applies supplier lead times, calendar & macroeconomic indicators,
and physical inventory simulation with fixed random seed (RANDOM_SEED = 42).
Can be executed as standalone module:
    python -m ml.data_generation.generate_synthetic_data
"""

import sys
from pathlib import Path
import pandas as pd

from ml.data_generation.synthetic_supplier import generate_supplier_attributes
from ml.data_generation.synthetic_business_features import generate_calendar_and_economic_features
from ml.data_generation.synthetic_inventory import simulate_inventory_flow

RANDOM_SEED: int = 42


def enrich_dataset_with_synthetic_dimensions(
    df: pd.DataFrame,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Enrich the base real-data foundation with required synthetic business dimensions.

    Pipeline:
        1. Supplier lead time & vendor IDs
        2. Calendar holidays, CPI proxy & regional events
        3. Physically coupled inventory flow simulation

    Args:
        df: Input dataframe mapped to canonical column names.
        random_seed: Seed for all random processes (default: 42).

    Returns:
        Fully augmented dataframe with both real and synthetic columns.
    """
    print(f"[DataGeneration] Starting synthetic dimension enrichment (Seed={random_seed})...")

    # Step 1: Supplier & Lead Time
    print("  -> Generating category-grounded supplier lead times...")
    df_supp = generate_supplier_attributes(df, random_seed=random_seed)

    # Step 2: Calendar Holidays, Economic Proxy, Regional Events
    print("  -> Generating calendar holidays and macroeconomic indices...")
    df_econ = generate_calendar_and_economic_features(df_supp, random_seed=random_seed)

    # Step 3: Physical Inventory Flow Simulation
    print("  -> Simulating demand-coupled physical inventory transitions...")
    df_inv = simulate_inventory_flow(df_econ, random_seed=random_seed)

    print(f"[DataGeneration] Completed enrichment. Augmented shape: {df_inv.shape}")
    return df_inv


if __name__ == "__main__":
    # Test script run on base retail store inventory if available
    raw_path = Path("data/raw/kaggle/retail_store_inventory.csv")
    if not raw_path.exists():
        print(f"Error: {raw_path} does not exist.")
        sys.exit(1)

    raw_df = pd.read_csv(raw_path)
    # Quick canonical rename for testing
    col_map = {
        "Date": "date",
        "Store ID": "store_id",
        "Product ID": "product_id",
        "Category": "category",
        "Region": "region",
        "Inventory Level": "raw_inventory_level",
        "Units Sold": "units_sold",
        "Units Ordered": "raw_units_ordered",
        "Demand Forecast": "raw_demand_forecast",
        "Price": "unit_price",
        "Discount": "discount",
        "Weather Condition": "weather",
        "Holiday/Promotion": "promotion",
        "Competitor Pricing": "competitor_price",
        "Seasonality": "seasonality",
    }
    base_df = raw_df.rename(columns=col_map)
    base_df["discount"] = base_df["discount"] / 100.0
    augmented = enrich_dataset_with_synthetic_dimensions(base_df, random_seed=RANDOM_SEED)

    print("\nSample Output:")
    print(augmented[["date", "store_id", "product_id", "units_sold", "supplier_lead_time", "inventory_level", "safety_stock", "reorder_point", "stockout_units"]].head(10))
