# views.py
from typing import List, Dict

from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from backend.api.services import get_ml_prediction
from .utils import generate_quiz_questions
from .models import Quiz, UserQuizProgress
from .schemas import (
    QuizCreateSchema,
    QuizResponseSchema,
    ErrorResponseSchema,
    QuizSubmitResponseSchema,
    QuizSubmitSchema
)

quiz_router = Router(tags=["Quiz"])


@quiz_router.post("/", response={201: QuizResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def create_quiz(request, payload: QuizCreateSchema):
    try:
        questions = generate_quiz_questions(get_ml_prediction)

        if not questions:
            return 400, {"error": "Failed to generate questions"}

        quiz = Quiz.objects.create(
            title=payload.title,
            description=payload.description,
            quiz_type=payload.quiz_type,
            difficulty=payload.difficulty,
            created_by=request.user,
            questions=questions
        )

        return 201, {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "quiz_type": quiz.quiz_type,
            "difficulty": quiz.difficulty,
            "created_by": quiz.created_by.username,
            "questions": questions
        }

    except Exception as e:
        return 400, {"error": str(e)}


@quiz_router.get("/", response={200: List[QuizResponseSchema], 400: ErrorResponseSchema}, auth=AuthBearer())
def get_quizzes(request):
    quizzes = Quiz.objects.all()
    return 200, [{
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "quiz_type": quiz.quiz_type,
        "difficulty": quiz.difficulty,
        "created_by": quiz.created_by.username,
        "questions": quiz.questions
    } for quiz in quizzes]


@quiz_router.get("/{quiz_id}", response={200: QuizResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def get_quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return 200, {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "quiz_type": quiz.quiz_type,
        "difficulty": quiz.difficulty,
        "created_by": quiz.created_by.username,
        "questions": quiz.questions
    }
