from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from backend.api.auth import ApiAuth
from backend.api.services import get_ml_prediction
from .models import Quiz, UserQuizProgress
from .schemas import (
    QuizCreateSchema,
    QuizResponseSchema,
    ErrorResponseSchema, QuizSubmitResponseSchema, QuizSubmitSchema
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


@quiz_router.post("/{quiz_id}",
                  response={200: QuizSubmitResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def submit_quiz(request, quiz_id: int, payload: QuizSubmitSchema):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not payload.answers:
        return 400, {"error": "No answers provided"}

    ml_response = get_ml_prediction(payload.answers)
    if 'predictions' not in ml_response:
        return 400, {"error": "Failed to get ML predictions or invalid token"}
    return 200, {"diseases": ml_response["predictions"]}
