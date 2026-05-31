from app.config import RUBRICS_DIR


def get_available_rubrics():

    rubric_files = []

    for file in RUBRICS_DIR.glob("*.json"):

        rubric_files.append(file.name)

    return rubric_files