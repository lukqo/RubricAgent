from pathlib import Path
from app.rubric_manager import get_available_rubrics

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from app.evaluator import evaluate_student
from app.schemas import EvaluationResponse
from app.config import (
    UPLOADS_DIR,
    DEFAULT_RUBRIC
)

app = FastAPI(
    title="RubricAgent",
    description="AI-powered rubric evaluation system",
    version="1.0.0"
)

UPLOADS_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():

    return {
        "message": "RubricAgent API funcionando"
    }


@app.get("/rubrics")
def list_rubrics():

    return {
        "rubrics": get_available_rubrics()
    }

@app.post(
    "/evaluate",
    response_model=EvaluationResponse
)
async def evaluate_code(
    student_name: str = Form(...),
    file: UploadFile = File(...),
    rubric_name: str = Form(...)
):

    try:

        # Crear path
        file_path = UPLOADS_DIR / file.filename

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Evaluar
        result = evaluate_student(
            student_name=student_name,
            file_path=str(file_path),
            rubric_name=rubric_name
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )