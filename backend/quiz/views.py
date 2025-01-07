from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from backend.api.services import get_ml_prediction
from .models import Quiz, UserQuizProgress
from .schemas import (
    QuizCreateSchema,
    QuizSubmitSchema,
    QuizResultSchema,
    QuizResponseSchema,
    ErrorResponseSchema,
    QuizSubmitResponseSchema, QuizCreateResponseSchema
)
from .utils import generate_quiz_questions

quiz_router = Router(tags=["Quiz"])


def remove_disease_probabilities(questions):
    cleaned_questions = []
    for question in questions:
        cleaned_question = question.copy()
        cleaned_question['diseases'] = list(question['diseases'].keys())
        cleaned_questions.append(cleaned_question)
    return cleaned_questions


@quiz_router.post("/", response={201: QuizCreateResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
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
        "questions": remove_disease_probabilities(quiz.questions)
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
        "questions": remove_disease_probabilities(quiz.questions)
    }


@quiz_router.post("/{quiz_id}/submit", response={200: QuizSubmitResponseSchema, 400: ErrorResponseSchema},
                  auth=AuthBearer())
def submit_quiz(request, quiz_id: int, payload: QuizSubmitSchema):
    try:
        quiz = get_object_or_404(Quiz, id=quiz_id)

        total_questions = len(quiz.questions)
        correct_answers = 0

        for i, user_answer in enumerate(payload.answers):
            question = quiz.questions[i]
            if set(user_answer.get('answer', [])) == set(question.get('symptoms', [])) or \
                    set(user_answer.get('answer', [])) == set(question.get('diseases', {}).keys()):
                correct_answers += 1

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        UserQuizProgress.objects.create(
            user=request.user,
            quiz=quiz,
            answers=payload.answers,
            score=score
        )

        return 200, {"score": score}

    except Exception as e:
        return 400, {"error": str(e)}


@quiz_router.get("/{quiz_id}/results", response={200: QuizResultSchema, 404: ErrorResponseSchema}, auth=AuthBearer())
def get_quiz_result(request, quiz_id: int):
    try:
        result = get_object_or_404(
            UserQuizProgress,
            user=request.user,
            quiz_id=quiz_id
        )

        return 200, {
            "quiz_id": result.quiz.id,
            "score": result.score,
            "answers": result.answers,
            "completed_at": result.completed_at.isoformat()
        }
    except UserQuizProgress.DoesNotExist:
        return 404, {"error": "Quiz result not found"}
