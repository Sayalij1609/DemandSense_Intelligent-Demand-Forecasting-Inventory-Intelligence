"""DemandSense Phase 1 reproducible data pipeline package."""


def run_pipeline(*args, **kwargs):
    """Lazy import and execution of master data pipeline."""
    from ml.data_pipeline.pipeline import run_pipeline as _run
    return _run(*args, **kwargs)


__all__ = ["run_pipeline"]
