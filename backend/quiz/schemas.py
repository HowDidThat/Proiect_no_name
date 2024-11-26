from ninja import Schema
from typing import Dict, List


class QuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuizSubmitSchema(Schema):
    answers: List[str]


class QuizResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuizSubmitResponseSchema(Schema):
    diseases: Dict[str, float]


class ErrorResponseSchema(Schema):
    error: str
