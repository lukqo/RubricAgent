from pydantic import BaseModel
from typing import List


class CriterionResult(BaseModel):
    criterion_id: int
    criterion_name: str
    level: str
    score: int
    feedback: str


class EvaluationResponse(BaseModel):
    student_name: str
    criteria_results: List[CriterionResult]
    total_score: int
    general_feedback: str