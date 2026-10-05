"""DemandSense synthetic supporting data generation package.

Provides reproducible, domain-grounded generation of missing business dimensions
(supplier lead time, physically coupled inventory dynamics, calendar holidays)
to augment real Kaggle sales data without overwriting raw observations.
"""

from ml.data_generation.synthetic_supplier import generate_supplier_attributes
from ml.data_generation.synthetic_inventory import simulate_inventory_flow
from ml.data_generation.synthetic_business_features import generate_calendar_and_economic_features

__all__ = [
    "generate_supplier_attributes",
    "simulate_inventory_flow",
    "generate_calendar_and_economic_features",
]
