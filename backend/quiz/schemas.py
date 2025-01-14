from typing import Dict, List, Union

from ninja import Schema


class QuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuestionSymptomsSchema(Schema):
    symptoms: List[str]


class CustomQuizCreateSchema(Schema):
    title: str
    description: str
    quiz_type: str
    difficulty: str
    questions: List[QuestionSymptomsSchema]


class QuizSubmitSchema(Schema):
    answers: List[Dict[str, List[str]]]


class QuizCreateResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str
    created_by: str
    questions: List[Dict[str, Union[List[str], Dict[str, float]]]]


class QuizResponseSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str
    created_by: str
    questions: List[Dict[str, List[str]]]


class QuizSubmitResponseSchema(Schema):
    score: float


class ErrorResponseSchema(Schema):
    error: str


class QuizResultSchema(Schema):
    quiz_id: int
    score: float
    answers: List[Dict[str, List[str]]]
    completed_at: str
