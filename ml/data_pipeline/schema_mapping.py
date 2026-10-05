"""Canonical schema definition and column mapping executor.

Loads explicit schema mapping rules and applies column renaming,
type casting, and standardizations to ensure schema compliance.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd


def load_schema_mapping(mapping_path: Path = Path("data/metadata/schema_mapping.json")) -> List[Dict[str, Any]]:
    """Load schema mapping definitions from metadata JSON."""
    with open(mapping_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["mappings"]


def apply_canonical_mapping(df: pd.DataFrame, source_name: str = "retail_store_inventory.csv") -> pd.DataFrame:
    """Transform source Kaggle dataframe to canonical column naming and standardized types.

    Args:
        df: Raw input dataframe from source CSV.
        source_name: Name of source dataset to filter mappings.

    Returns:
        Dataframe adhering to DemandSense canonical schema conventions.
    """
    df = df.copy()

    # Explicit direct mapping dictionary for retail_store_inventory.csv
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

    # Rename existing columns
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    # Standardize data types
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    if "discount" in df.columns:
        # Convert integer percentage (0, 5, 10, 15, 20) to decimal rate (0.00 - 0.20)
        df["discount"] = (df["discount"] / 100.0).round(2)

    if "weather" in df.columns:
        df["weather"] = df["weather"].str.lower().str.strip()

    if "unit_price" in df.columns:
        df["unit_price"] = df["unit_price"].astype(float).round(2)

    if "competitor_price" in df.columns:
        df["competitor_price"] = df["competitor_price"].astype(float).round(2)

    if "units_sold" in df.columns:
        df["units_sold"] = df["units_sold"].astype(int)

    if "promotion" in df.columns:
        df["promotion"] = df["promotion"].astype(int)

    return df
