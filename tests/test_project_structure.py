from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRECTORIES = [
    "ingest",
    "dbt",
    "models",
    "drift",
    "serving",
    "infra",
    "docs",
    "data",
    "tests",
    ".github",
]

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "pyproject.toml",
    "requirements-dev.txt",
    ".gitignore",
]


def test_required_directories_exist():
    """Check whether all required project directories exist."""
    missing_dirs = [
        directory for directory in REQUIRED_DIRECTORIES if not (PROJECT_ROOT / directory).is_dir()
    ]

    assert not missing_dirs, f"Missing directories: {missing_dirs}"


def test_required_files_exist():
    """Check whether all required project files exist."""
    missing_files = [file for file in REQUIRED_FILES if not (PROJECT_ROOT / file).is_file()]

    assert not missing_files, f"Missing files: {missing_files}"
