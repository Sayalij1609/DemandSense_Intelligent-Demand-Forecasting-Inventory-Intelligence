"""Calendar holiday and macro-economic feature enrichment module.

Generates deterministic national calendar holidays, consumer price trends,
and regional events to provide exogenous context for forecasting models.
"""

from typing import Set
import numpy as np
import pandas as pd

MAJOR_HOLIDAYS_SET: Set[str] = {
    # 2022 Holidays
    "2022-01-01", "2022-01-17", "2022-02-14", "2022-02-21", "2022-04-17",
    "2022-05-08", "2022-05-30", "2022-06-19", "2022-06-20", "2022-07-04",
    "2022-09-05", "2022-10-31", "2022-11-11", "2022-11-24", "2022-11-25",
    "2022-12-24", "2022-12-25", "2022-12-26", "2022-12-31",
    # 2023 Holidays
    "2023-01-01", "2023-01-02", "2023-01-16", "2023-02-14", "2023-02-20",
    "2023-04-09", "2023-05-14", "2023-05-29", "2023-06-19", "2023-07-04",
    "2023-09-04", "2023-10-31", "2023-11-10", "2023-11-11", "2023-11-23",
    "2023-11-24", "2023-12-24", "2023-12-25", "2023-12-31",
    # 2024 Holidays
    "2024-01-01",
}


def generate_calendar_and_economic_features(df: pd.DataFrame, random_seed: int = 42) -> pd.DataFrame:
    """Enrich dataset with calendar holidays, economic indices, and regional events.

    Args:
        df: Input dataframe containing 'date', 'region', 'seasonality'.
        random_seed: Random seed for reproducibility.

    Returns:
        Dataframe augmented with 'holiday', 'economic_indicator', and 'regional_event'.
    """
    df = df.copy()
    dates_str = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # 1. Deterministic statutory holiday mapping
    df["holiday"] = dates_str.isin(MAJOR_HOLIDAYS_SET).astype(int)

    # 2. Economic Indicator: Macro Consumer Price Index (CPI) Proxy
    # Modeled after actual US 2022-2023 headline CPI trajectory (281.0 in Jan 2022 to 307.0 in Dec 2023)
    dt_series = pd.to_datetime(df["date"])
    days_elapsed = (dt_series - pd.Timestamp("2022-01-01")).dt.days
    total_days = 731.0
    cpi_proxy = 281.0 + (26.0 * (days_elapsed / total_days)) + np.sin(days_elapsed / 30.0) * 0.8
    df["economic_indicator"] = np.round(cpi_proxy, 2)

    # 3. Regional Event Indicator:
    # Captures localized demand surges (e.g. regional expo, back-to-school fair, seasonal festival)
    rng = np.random.default_rng(random_seed)
    # Regional events occur with ~8% probability, correlated with seasons/weekends
    is_weekend = dt_series.dt.dayofweek.isin([5, 6])
    event_prob = np.where(is_weekend, 0.12, 0.05)
    df["regional_event"] = (rng.random(len(df)) < event_prob).astype(int)

    return df
