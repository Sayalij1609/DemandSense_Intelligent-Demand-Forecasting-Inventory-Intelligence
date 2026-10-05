"""Supplier lead-time and vendor assignment module.

Generates category-grounded, product-level baseline supplier lead times
with subtle operational variance reflecting logistics conditions (weather, holidays).
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd

CATEGORY_BASE_LEAD_TIME: Dict[str, int] = {
    "Groceries": 3,
    "Clothing": 5,
    "Toys": 7,
    "Electronics": 9,
    "Furniture": 14,
}

CATEGORY_LEAD_TIME_BOUNDS: Dict[str, Tuple[int, int]] = {
    "Groceries": (2, 5),
    "Clothing": (4, 8),
    "Toys": (5, 10),
    "Electronics": (7, 13),
    "Furniture": (10, 18),
}

PRODUCT_SUPPLIER_MAP: Dict[str, str] = {
    # Groceries
    "P0001": "SUPP-GROC-01",
    "P0002": "SUPP-GROC-01",
    "P0003": "SUPP-GROC-02",
    "P0004": "SUPP-GROC-02",
    # Clothing
    "P0005": "SUPP-CLOTH-01",
    "P0006": "SUPP-CLOTH-01",
    "P0007": "SUPP-CLOTH-02",
    "P0008": "SUPP-CLOTH-02",
    # Electronics
    "P0009": "SUPP-ELEC-01",
    "P0010": "SUPP-ELEC-01",
    "P0011": "SUPP-ELEC-02",
    "P0012": "SUPP-ELEC-02",
    # Furniture
    "P0013": "SUPP-FURN-01",
    "P0014": "SUPP-FURN-01",
    "P0015": "SUPP-FURN-02",
    "P0016": "SUPP-FURN-02",
    # Toys
    "P0017": "SUPP-TOYS-01",
    "P0018": "SUPP-TOYS-01",
    "P0019": "SUPP-TOYS-02",
    "P0020": "SUPP-TOYS-02",
}


def generate_supplier_attributes(df: pd.DataFrame, random_seed: int = 42) -> pd.DataFrame:
    """Assign stable supplier identifiers and realistic supplier lead times to each record.

    Lead time represents the elapsed calendar days between order placement and receipt.
    Each product maintains a stable baseline lead time determined by its physical category,
    with bounded +/- 1 day perturbations during severe weather (snow) or holiday shipping congestion.

    Args:
        df: Input dataframe containing 'product_id', 'category', 'weather', 'promotion'.
        random_seed: Random seed for reproducibility.

    Returns:
        Dataframe augmented with 'supplier_id' and 'supplier_lead_time' columns.
    """
    rng = np.random.default_rng(random_seed)
    df = df.copy()

    # 1. Assign deterministic supplier ID
    df["supplier_id"] = df["product_id"].map(PRODUCT_SUPPLIER_MAP).fillna("SUPP-GEN-01")

    # 2. Assign base lead time per category
    base_lead_times = df["category"].map(CATEGORY_BASE_LEAD_TIME).fillna(7).astype(int)

    # 3. Model operational logistics perturbations:
    # - Severe weather (Snowy) delays ground transportation by +1 day (70% probability)
    # - High holiday/promotional periods delay logistics by +1 day (50% probability)
    weather_delay = np.where(
        (df["weather"].str.lower() == "snowy") & (rng.random(len(df)) < 0.70),
        1,
        0,
    )
    holiday_delay = np.where(
        (df["promotion"] == 1) & (rng.random(len(df)) < 0.50),
        1,
        0,
    )

    lead_times = base_lead_times + weather_delay + holiday_delay

    # Apply strict physical category bounds
    bounded_lead_times = []
    for cat, lt in zip(df["category"], lead_times):
        min_lt, max_lt = CATEGORY_LEAD_TIME_BOUNDS.get(cat, (2, 20))
        bounded_lead_times.append(int(np.clip(lt, min_lt, max_lt)))

    df["supplier_lead_time"] = bounded_lead_times
    return df
