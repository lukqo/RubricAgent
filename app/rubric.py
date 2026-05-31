import json

from app.config import RUBRICS_DIR


def load_rubric(rubric_name: str) -> dict:

    rubric_path = RUBRICS_DIR / rubric_name

    if not rubric_path.exists():
        raise FileNotFoundError(
            f"Rúbrica no encontrada: {rubric_name}"
        )

    with open(rubric_path, "r", encoding="utf-8") as file:
        return json.load(file)