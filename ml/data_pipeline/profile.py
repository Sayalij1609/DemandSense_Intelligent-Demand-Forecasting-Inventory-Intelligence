"""Dataset profiling module.

Inspects all raw Kaggle CSV files, extracts structural metadata,
null distributions, uniqueness statistics, and temporal spans.
"""

import glob
import json
import os
from pathlib import Path
from typing import Any, Dict
import numpy as np
import pandas as pd


def _safe_convert(val: Any) -> Any:
    """Ensure value is JSON serializable."""
    if pd.isna(val):
        return None
    if isinstance(val, (np.integer, int)):
        return int(val)
    if isinstance(val, (np.floating, float)):
        return float(val)
    if isinstance(val, (np.bool_, bool)):
        return bool(val)
    return str(val)


def profile_single_csv(file_path: Path) -> Dict[str, Any]:
    """Profile a single CSV file safely handling multiple encodings."""
    filename = file_path.name
    encodings = ["utf-8", "ISO-8859-1", "latin1", "cp1252"]
    df = None
    used_encoding = None

    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc, nrows=50000)
            used_encoding = enc
            break
        except Exception:
            continue

    if df is None:
        return {"filename": filename, "error": "Unable to read with supported encodings"}

    try:
        with open(file_path, "r", encoding=used_encoding, errors="ignore") as f:
            total_rows = sum(1 for _ in f) - 1
    except Exception:
        total_rows = len(df)

    date_cols = []
    min_date, max_date = {}, {}
    for col in df.columns:
        col_lower = str(col).lower()
        if any(d in col_lower for d in ["date", "time", "day", "month", "year", "period"]):
            date_cols.append(col)
            try:
                dt_series = pd.to_datetime(df[col], errors="coerce").dropna()
                if len(dt_series) > 0:
                    min_date[col] = str(dt_series.min())
                    max_date[col] = str(dt_series.max())
            except Exception:
                pass

    unique_counts = {col: int(df[col].nunique()) for col in df.columns}
    missing_counts = {col: int(df[col].isnull().sum()) for col in df.columns}
    missing_pct = {col: round(float(df[col].isnull().mean() * 100), 2) for col in df.columns}

    num_cols = list(df.select_dtypes(include=[np.number]).columns)
    cat_cols = [c for c in df.columns if c not in num_cols]

    sample_records = []
    for r in df.head(3).to_dict(orient="records"):
        sample_records.append({k: _safe_convert(v) for k, v in r.items()})

    return {
        "filename": filename,
        "total_rows": total_rows,
        "sample_rows_analyzed": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "encoding": used_encoding,
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_counts": missing_counts,
        "missing_pct": missing_pct,
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "date_columns": date_cols,
        "min_date": min_date,
        "max_date": max_date,
        "unique_counts": unique_counts,
        "sample": sample_records,
    }


def run_profiling(raw_dir: Path = Path("data/raw/kaggle"), output_dir: Path = Path("data/metadata")) -> Dict[str, Any]:
    """Profile all CSV files in raw_dir and persist JSON profile artifact."""
    output_dir.mkdir(parents=True, exist_ok=True)
    profiles = {}

    csv_files = sorted(raw_dir.glob("*.csv"))
    print(f"[Profiler] Profiling {len(csv_files)} CSV datasets from {raw_dir}...")

    for csv_file in csv_files:
        profile = profile_single_csv(csv_file)
        profiles[profile["filename"]] = profile

    out_file = output_dir / "dataset_profiles.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    print(f"[Profiler] Successfully saved dataset profiles to {out_file}")
    return profiles


if __name__ == "__main__":
    run_profiling()
