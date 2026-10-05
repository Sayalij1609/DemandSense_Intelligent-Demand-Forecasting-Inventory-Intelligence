"""Unified dataset builder and export module.

Aligns columns to the DemandSense canonical schema and writes optimized
Parquet and CSV artifacts to data/processed/.
"""

from pathlib import Path
import pandas as pd

CANONICAL_COLUMN_ORDER = [
    # Core target schema
    "date",
    "product_id",
    "store_id",
    "category",
    "units_sold",
    "unit_price",
    "discount",
    "promotion",
    "holiday",
    "inventory_level",
    "supplier_lead_time",
    # Optional & contextual business dimensions
    "weather",
    "competitor_price",
    "economic_indicator",
    "regional_event",
    "region",
    "seasonality",
    "supplier_id",
    # Inventory decision ground truth & simulation audit trails
    "safety_stock",
    "reorder_point",
    "stockout_units",
    "replenishment_received",
    # Preserved raw Kaggle fields for verification
    "raw_inventory_level",
    "raw_units_ordered",
    "raw_demand_forecast",
]


def assemble_and_export_dataset(
    df: pd.DataFrame,
    output_dir: Path = Path("data/processed"),
    base_name: str = "demandsense_dataset",
) -> Path:
    """Reorder columns to canonical schema and export Parquet and CSV artifacts.

    Args:
        df: Augmented unified dataframe.
        output_dir: Directory where processed files will be written.
        base_name: Base filename prefix.

    Returns:
        Path to the primary Parquet file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Reorder columns: canonical first, followed by any remaining columns
    existing_cols = [c for c in CANONICAL_COLUMN_ORDER if c in df.columns]
    extra_cols = [c for c in df.columns if c not in existing_cols]
    final_cols = existing_cols + extra_cols
    df_ordered = df[final_cols].copy()

    # Sort deterministically
    df_ordered = df_ordered.sort_values(["date", "store_id", "product_id"]).reset_index(drop=True)

    parquet_path = output_dir / f"{base_name}.parquet"
    csv_path = output_dir / f"{base_name}.csv"

    print(f"[DatasetBuilder] Writing Parquet to {parquet_path}...")
    df_ordered.to_parquet(parquet_path, index=False, engine="pyarrow", compression="snappy")

    print(f"[DatasetBuilder] Writing CSV to {csv_path}...")
    df_ordered.to_csv(csv_path, index=False, encoding="utf-8")

    parquet_size_mb = parquet_path.stat().st_size / (1024 * 1024)
    csv_size_mb = csv_path.stat().st_size / (1024 * 1024)

    print(
        f"[DatasetBuilder] Artifacts exported successfully:\n"
        f"  - Parquet: {parquet_path} ({parquet_size_mb:.2f} MB, {len(df_ordered)} rows, {len(df_ordered.columns)} cols)\n"
        f"  - CSV:     {csv_path} ({csv_size_mb:.2f} MB)"
    )
    return parquet_path
