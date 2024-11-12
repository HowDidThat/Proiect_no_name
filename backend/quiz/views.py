from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from .models import Quiz
from .schemas import (
    QuizCreateSchema,
    QuizResponseSchema,
    ErrorResponseSchema
)

quiz_router = Router(tags=["Quiz"])


@quiz_router.post("/", response=QuizResponseSchema, auth=AuthBearer())
def create_quiz(request, payload: QuizCreateSchema):
    quiz = Quiz.objects.create(
        title=payload.title,
        description=payload.description,
        quiz_type=payload.quiz_type,
        difficulty=payload.difficulty
    )
    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "quiz_type": quiz.quiz_type,
        "difficulty": quiz.difficulty
    }


@quiz_router.get("/", response={200: List[QuizResponseSchema], 400: ErrorResponseSchema}, auth=AuthBearer())
def get_quizzes(request):
    quizzes = Quiz.objects.all()
    return 200, [{"id": quiz.id, "title": quiz.title, "description": quiz.description, "quiz_type": quiz.quiz_type,
                  "difficulty": quiz.difficulty} for quiz in quizzes]


@quiz_router.get("/{quiz_id}", response={200: QuizResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def get_quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return 200, {"id": quiz.id, "title": quiz.title, "description": quiz.description, "quiz_type": quiz.quiz_type,
                 "difficulty": quiz.difficulty}
