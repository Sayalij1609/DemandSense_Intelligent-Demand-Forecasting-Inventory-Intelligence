"""Verification tests for the project foundation structure."""
from pathlib import Path


def test_required_directories_exist():
    """Verify that all core foundational directories exist."""
    root = Path(__file__).resolve().parent.parent

    required_dirs = [
        "backend",
        "frontend",
        "ml",
        "data",
        "tests",
        "docker",
        "docs",
    ]

    for dir_name in required_dirs:
        target_dir = root / dir_name
        assert target_dir.exists(), f"Missing required directory: {dir_name}"
        assert target_dir.is_dir(), f"{dir_name} is not a directory"


def test_required_root_files_exist():
    """Verify that all root configuration and documentation files exist."""
    root = Path(__file__).resolve().parent.parent

    required_files = [
        ".env.example",
        ".gitignore",
        "docker-compose.yml",
        "README.md",
    ]

    for file_name in required_files:
        target_file = root / file_name
        assert target_file.exists(), f"Missing required root file: {file_name}"
        assert target_file.is_file(), f"{file_name} is not a file"


def test_independent_dependency_management():
    """Verify that backend, ML, and frontend maintain independent dependency manifests."""
    root = Path(__file__).resolve().parent.parent

    assert (root / "backend" / "requirements.txt").exists(), "Missing backend/requirements.txt"
    assert (root / "ml" / "requirements.txt").exists(), "Missing ml/requirements.txt"
    assert (root / "frontend" / "package.json").exists(), "Missing frontend/package.json"
