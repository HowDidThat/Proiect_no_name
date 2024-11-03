from ninja import Schema
from typing import Dict


class QuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuizSubmitSchema(Schema):
    answers: Dict


class QuizResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuizSubmitResponseSchema(Schema):
    score: float


class ErrorResponseSchema(Schema):
    error: str
