from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from .models import Quiz, UserQuizProgress
from .schemas import (
    QuizCreateSchema,
    QuizSubmitSchema,
    QuizResponseSchema,
    QuizSubmitResponseSchema,
    ErrorResponseSchema
)

quiz_router = Router()


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


@quiz_router.post("/{quiz_id}", response={200: QuizSubmitResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def submit_quiz(request, quiz_id: int, payload: QuizSubmitSchema):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not payload.answers:
        return 400, {"error": "No answers provided"}

    score = 75.0

    UserQuizProgress.objects.create(
        user=request.user,
        quiz=quiz,
        answers=payload.answers,
        score=score
    )

    return 200, {"score": score}
