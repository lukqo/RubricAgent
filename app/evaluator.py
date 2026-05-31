from pathlib import Path

from app.notebook_parser import extract_code_from_notebook
from app.prompt_builder import build_evaluation_prompt
from app.llm_client import evaluate_with_llm
from app.rubric import load_rubric
from app.response_parser import normalize_response


def validate_file_extension(
    file_extension: str,
    rubric: dict
):

    allowed_extensions = rubric.get(
        "allowed_extensions",
        []
    )

    if file_extension not in allowed_extensions:

        raise ValueError(
            f"""
Extensión no permitida.

Extensión recibida:
{file_extension}

Extensiones permitidas:
{allowed_extensions}
"""
        )


def read_code_file(file_path: str) -> str:

    path = Path(file_path)

    if path.suffix == ".py":

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    elif path.suffix == ".ipynb":

        return extract_code_from_notebook(
            file_path
        )

    else:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()


def fix_scores_from_rubric(
    normalized_result: dict,
    rubric: dict
) -> dict:

    criteria = rubric.get("criteria", [])

    # Construir mapa: criterion_id -> levels con puntajes
    rubric_map = {}
    for criterion in criteria:
        cid = criterion.get("id")
        levels = criterion.get("levels", {})
        rubric_map[cid] = levels

    print("DEBUG rubric_map keys:", list(rubric_map.keys()))

    total_score = 0
    fixed_results = []

    for item in normalized_result.get("criteria_results", []):

        cid = item.get("criterion_id")
        level = item.get("level", "")

        # Buscar por criterion_id primero
        rubric_levels = rubric_map.get(cid, {})

        # Si no encuentra por id, busca por nombre del criterio
        if not rubric_levels:
            criterion_name = item.get("criterion_name", "").lower()
            for criterion in criteria:
                rubric_name = criterion.get("name", "").lower()
                if rubric_name in criterion_name or criterion_name in rubric_name:
                    rubric_levels = criterion.get("levels", {})
                    item["criterion_id"] = criterion.get("id", cid)
                    break

        real_score = item.get("score", 0)

        if level in rubric_levels:
            real_score = rubric_levels[level].get("points", real_score)

        item["score"] = real_score
        total_score += real_score
        fixed_results.append(item)

        print(f"DEBUG criterio {item['criterion_id']} - {item['criterion_name']} - level: {level} - score: {real_score}")

    normalized_result["criteria_results"] = fixed_results
    normalized_result["total_score"] = str(total_score)

    return normalized_result


def evaluate_student(
    student_name: str,
    file_path: str,
    rubric_name: str
) -> dict:

    rubric = load_rubric(
        rubric_name
    )

    file_extension = Path(
        file_path
    ).suffix

    validate_file_extension(
        file_extension=file_extension,
        rubric=rubric
    )

    code = read_code_file(
        file_path
    )

    prompt = build_evaluation_prompt(
        student_name=student_name,
        rubric=rubric,
        code=code
    )

    result = evaluate_with_llm(
        prompt=prompt,
        student_name=student_name
    )

    normalized_result = normalize_response(
        result
    )

    # Corregir puntajes desde la rúbrica real
    normalized_result = fix_scores_from_rubric(
        normalized_result=normalized_result,
        rubric=rubric
    )

    return normalized_result