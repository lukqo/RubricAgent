from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOADS_DIR = BASE_DIR / "uploads"

RUBRICS_DIR = BASE_DIR / "rubrics"

DEFAULT_RUBRIC = "default_rubric.json"

MAX_FILE_SIZE_MB = 10