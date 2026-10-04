"""Global pytest fixtures and configuration."""
import os
import sys
from pathlib import Path

# Add backend and ml to Python path for seamless testing
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))
sys.path.insert(0, str(ROOT_DIR / "ml"))
