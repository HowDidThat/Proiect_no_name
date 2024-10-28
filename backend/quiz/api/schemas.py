from ninja import Schema
from datetime import datetime
from typing import Optional, List


class UserSchema(Schema):
    id: int
    email: str
    institution: str
    year_of_study: int


class QuizSchema(Schema):
    id: int
    title: str
    description: str
    quiz_type: str
    difficulty: str


class QuestionSchema(Schema):
    id: int
    quiz_id: int
    content: str


class ProgressSchema(Schema):
    id: int
    user_id: int
    quiz_id: int
    score: float
    completed_at: datetime


class QuizStartRequest(Schema):
    quiz_type: str
    difficulty: str


class QuizSubmitRequest(Schema):
    answers: dict
