from typing import Dict, List

from ninja import Schema


class QuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str
    symptoms: List[str]


class QuizSubmitSchema(Schema):
    answers: List[str]


class QuizResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str
    symptoms: List[str]
    diseases: Dict[str, float]


class QuizSubmitResponseSchema(Schema):
    diseases: Dict[str, float]


class ErrorResponseSchema(Schema):
    error: str
