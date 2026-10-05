"""Synthetic dimension augmentation pipeline step.

Coordinates execution of reproducible data generation modules to append
physically coupled inventory dynamics, supplier lead times, and calendar indicators.
"""

import pandas as pd
from ml.data_generation.generate_synthetic_data import enrich_dataset_with_synthetic_dimensions


def run_synthetic_generation(df_real: pd.DataFrame, random_seed: int = 42) -> pd.DataFrame:
    """Enrich the real-data foundation with synthetic supporting dimensions.

    Args:
        df_real: The mapped real-data foundation dataframe.
        random_seed: Seed ensuring strict reproducibility (default: 42).

    Returns:
        Dataframe containing unified real and synthetic attributes.
    """
    print(f"[SyntheticPipeline] Appending missing dimensions using RANDOM_SEED={random_seed}...")
    df_augmented = enrich_dataset_with_synthetic_dimensions(df_real, random_seed=random_seed)
    return df_augmented
