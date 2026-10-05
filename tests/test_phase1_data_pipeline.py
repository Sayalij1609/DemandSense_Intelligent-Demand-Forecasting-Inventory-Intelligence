"""Verification tests for Phase 1 Data Pipeline and Unified Dataset."""
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_metadata_artifacts_exist():
    """Verify all Phase 1 metadata files exist."""
    metadata_dir = ROOT / "data" / "metadata"
    assert (metadata_dir / "dataset_catalog.json").exists()
    assert (metadata_dir / "dataset_profiles.json").exists()
    assert (metadata_dir / "source_data_dictionary.md").exists()
    assert (metadata_dir / "schema_mapping.json").exists()
    assert (metadata_dir / "synthetic_data_catalog.json").exists()


def test_reports_exist():
    """Verify all Phase 1 reports exist."""
    reports_dir = ROOT / "data" / "reports"
    assert (reports_dir / "phase1_dataset_analysis.md").exists()
    assert (reports_dir / "final_dataset_quality_report.md").exists()
    assert (reports_dir / "data_lineage_report.md").exists()


def test_docs_exist():
    """Verify all Phase 1 documentation exists in docs/data/."""
    docs_dir = ROOT / "docs" / "data"
    assert (docs_dir / "dataset_overview.md").exists()
    assert (docs_dir / "data_dictionary.md").exists()
    assert (docs_dir / "data_lineage.md").exists()
    assert (docs_dir / "integration_strategy.md").exists()
    assert (docs_dir / "synthetic_data_methodology.md").exists()


def test_processed_dataset_artifacts():
    """Verify output dataset exists in both Parquet and CSV formats."""
    processed_dir = ROOT / "data" / "processed"
    parquet_path = processed_dir / "demandsense_dataset.parquet"
    csv_path = processed_dir / "demandsense_dataset.csv"

    assert parquet_path.exists(), "Missing demandsense_dataset.parquet"
    assert csv_path.exists(), "Missing demandsense_dataset.csv"


def test_dataset_quality_and_schema():
    """Verify canonical schema, dimensions, and data integrity of the unified dataset."""
    parquet_path = ROOT / "data" / "processed" / "demandsense_dataset.parquet"
    df = pd.read_parquet(parquet_path)

    # Required canonical columns
    canonical_cols = [
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
    ]
    for col in canonical_cols:
        assert col in df.columns, f"Missing required column: {col}"

    # Dimensional assertions
    assert len(df) == 73100, f"Expected 73,100 rows, got {len(df)}"
    assert df["store_id"].nunique() == 5, "Expected 5 unique stores"
    assert df["product_id"].nunique() == 20, "Expected 20 unique products"
    assert df["category"].nunique() == 5, "Expected 5 unique categories"
    assert df["date"].nunique() == 731, "Expected 731 unique dates"

    # Integrity assertions
    assert not df[canonical_cols].isnull().any().any(), "Detected null values in core columns"
    assert (df["units_sold"] >= 0).all(), "Detected negative units_sold"
    assert (df["unit_price"] > 0).all(), "Detected non-positive unit_price"
    assert (df["inventory_level"] >= 0).all(), "Detected negative inventory_level"
    assert (df["supplier_lead_time"] > 0).all(), "Detected non-positive supplier_lead_time"

    # Business key uniqueness
    dups = df.duplicated(subset=["date", "store_id", "product_id"]).sum()
    assert dups == 0, f"Found {dups} duplicate business keys"
