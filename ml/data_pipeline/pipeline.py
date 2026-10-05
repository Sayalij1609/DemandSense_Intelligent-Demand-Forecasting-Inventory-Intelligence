"""Master reproducible Phase 1 data pipeline orchestrator.

Executes the complete end-to-end data acquisition, profiling, integration,
synthetic augmentation, export, and validation workflow.

Run via:
    python -m ml.data_pipeline.pipeline
"""

import sys
import time
from pathlib import Path

from ml.data_pipeline.profile import run_profiling
from ml.data_pipeline.integrate import load_and_integrate_real_data
from ml.data_pipeline.generate_synthetic import run_synthetic_generation
from ml.data_pipeline.build_dataset import assemble_and_export_dataset
from ml.data_pipeline.validate import validate_unified_dataset

RANDOM_SEED: int = 42


def run_pipeline(
    raw_dir: Path = Path("data/raw/kaggle"),
    metadata_dir: Path = Path("data/metadata"),
    processed_dir: Path = Path("data/processed"),
    reports_dir: Path = Path("data/reports"),
    random_seed: int = RANDOM_SEED,
) -> None:
    """Execute the full reproducible Phase 1 pipeline."""
    start_time = time.time()
    print("=" * 80)
    print(" DEMANDSENSE PHASE 1: DATA ENGINEERING & UNIFIED DATASET PIPELINE")
    print("=" * 80)

    # Stage 1: Dataset Profiling
    print("\n[Stage 1/5] Profiling Raw Kaggle Datasets...")
    run_profiling(raw_dir=raw_dir, output_dir=metadata_dir)

    # Stage 2: Real Data Integration
    print("\n[Stage 2/5] Integrating Primary Real-Data Foundation...")
    primary_csv = raw_dir / "retail_store_inventory.csv"
    df_real = load_and_integrate_real_data(raw_csv_path=primary_csv)

    # Stage 3: Synthetic Dimension Augmentation
    print("\n[Stage 3/5] Generating Missing Business Dimensions...")
    df_augmented = run_synthetic_generation(df_real, random_seed=random_seed)

    # Stage 4: Assemble & Export Final Dataset
    print("\n[Stage 4/5] Assembling Canonical Schema and Exporting Artifacts...")
    parquet_path = assemble_and_export_dataset(df_augmented, output_dir=processed_dir)

    # Stage 5: Validation & Compliance Reporting
    print("\n[Stage 5/5] Running Quality Validations & Generating Reports...")
    metrics = validate_unified_dataset(df_augmented, report_dir=reports_dir)

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f" DEMANDSENSE PHASE 1 PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f}s")
    print(f" Output Parquet: {parquet_path}")
    print(f" Output CSV:     {processed_dir / 'demandsense_dataset.csv'}")
    print(f" Quality Report: {reports_dir / 'final_dataset_quality_report.md'}")
    print(f" Lineage Report: {reports_dir / 'data_lineage_report.md'}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed with error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
