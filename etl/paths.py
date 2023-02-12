import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("BASE_DIR", Path(__file__).parent.parent))
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"
INPUT_DIR = DATA_DIR / "input"
FIXED_INPUT_DIR = INPUT_DIR / "fixed"
INPUT_MAPPINGS = INPUT_DIR / "mappings"
INPUT_RECCOMENDATIONS = INPUT_DIR / "reccomendations"

# ETL-related paths
ETL_DIR = BASE_DIR / "etl"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
