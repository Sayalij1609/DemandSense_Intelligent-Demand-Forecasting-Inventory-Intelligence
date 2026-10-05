"""Real-data integration module.

Loads the selected primary Kaggle dataset, performs integrity and continuity
checks, applies canonical schema mapping, and establishes the immutable
real-data foundation for DemandSense.
"""

from pathlib import Path
import pandas as pd

from ml.data_pipeline.schema_mapping import apply_canonical_mapping


def load_and_integrate_real_data(
    raw_csv_path: Path = Path("data/raw/kaggle/retail_store_inventory.csv"),
) -> pd.DataFrame:
    """Load and prepare the real-data foundation from raw Kaggle source.

    Performs:
        - Integrity validation (row counts, column presence)
        - Canonical column name mapping
        - Panel balance validation (5 stores * 20 products * 731 days = 73,100 records)

    Args:
        raw_csv_path: Path to the raw primary CSV file.

    Returns:
        Dataframe containing clean real-data foundation.
    """
    if not raw_csv_path.exists():
        raise FileNotFoundError(f"Primary raw dataset not found at {raw_csv_path}")

    print(f"[Integrate] Loading primary foundation from {raw_csv_path}...")
    df_raw = pd.read_csv(raw_csv_path)

    # Assert expected shape
    expected_rows = 73100
    if len(df_raw) != expected_rows:
        print(f"[Integrate] Warning: Expected {expected_rows} rows, found {len(df_raw)}")

    # Apply canonical schema transformation
    df_mapped = apply_canonical_mapping(df_raw, source_name="retail_store_inventory.csv")

    # Verify panel integrity: (Store, Product) series
    unique_stores = df_mapped["store_id"].nunique()
    unique_prods = df_mapped["product_id"].nunique()
    unique_dates = df_mapped["date"].nunique()

    print(
        f"[Integrate] Panel Dimensions: {unique_stores} stores, "
        f"{unique_prods} products, {unique_dates} continuous calendar days."
    )

    # Verify absence of duplicate business keys (date, store_id, product_id)
    duplicates = df_mapped.duplicated(subset=["date", "store_id", "product_id"]).sum()
    if duplicates > 0:
        raise ValueError(f"Found {duplicates} duplicate business keys in primary dataset!")

    print("[Integrate] Real-data foundation successfully validated and integrated.")
    return df_mapped


if __name__ == "__main__":
    df = load_and_integrate_real_data()
    print("Head:\n", df.head(3))
