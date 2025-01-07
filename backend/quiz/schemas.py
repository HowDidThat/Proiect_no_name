from typing import Dict, List, Union

from ninja import Schema


class QuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuizSubmitSchema(Schema):
    answers: List[Dict[str, List[str]]]


class QuizResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str
    created_by: str
    questions: List[Dict[str, Union[List[str], Dict[str, float]]]]


class QuizSubmitResponseSchema(Schema):
    diseases: Dict[str, float]


class ErrorResponseSchema(Schema):
    error: str


class SymptomsListSchema(Schema):
    symptoms: List[str]

class DiseasesListSchema(Schema):
    diseases: List[str]