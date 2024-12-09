from typing import List, Dict

from django.shortcuts import get_object_or_404
from ninja import Router

from authentication.views import AuthBearer
from backend.api.services import get_ml_prediction
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
        ml_response = get_ml_prediction(payload.symptoms)

        if 'predictions' not in ml_response:
            return 400, {"error": "Failed to get ML predictions"}

        relevant_diseases = {
            disease: prob
            for disease, prob in ml_response["predictions"].items()
            if prob > 0
        }

        if not relevant_diseases:
            return 400, {"error": "No relevant diseases found for the given symptoms"}

        quiz = Quiz.objects.create(
            title=payload.title,
            description=payload.description,
            quiz_type=payload.quiz_type,
            difficulty=payload.difficulty,
            created_by=request.user,
            symptoms=payload.symptoms,
            diseases=relevant_diseases
        )

        return 201, {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "quiz_type": quiz.quiz_type,
            "difficulty": quiz.difficulty,
            "created_by": quiz.created_by.username,
            "symptoms": quiz.symptoms,
            "diseases": quiz.diseases
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
        "symptoms": quiz.symptoms,
        "diseases": quiz.diseases
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
        "symptoms": quiz.symptoms,
        "diseases": quiz.diseases
    }


@quiz_router.post("/{quiz_id}", response={200: QuizSubmitResponseSchema, 400: ErrorResponseSchema}, auth=AuthBearer())
def submit_quiz(request, quiz_id: int, payload: QuizSubmitSchema):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not payload.answers:
        return 400, {"error": "No answers provided"}

    results = []
    total_score = 0

    for idx, answer in enumerate(payload.answers):
        ml_response = get_ml_prediction(answer.get('symptoms', []))
        if 'predictions' not in ml_response:
            return 400, {"error": f"Failed to get ML predictions for answer {idx + 1}"}

        pair_score = calculate_score(
            quiz.symptom_disease_pairs[idx]['expected_diseases'],
            ml_response["predictions"]
        )
        total_score += pair_score
        results.append({
            "symptoms": answer.get('symptoms', []),
            "predictions": ml_response["predictions"],
            "score": pair_score
        })

    average_score = total_score / len(payload.answers)

    UserQuizProgress.objects.create(
        user=request.user,
        quiz=quiz,
        answers=payload.answers,
        score=average_score
    )

    return 200, {
        "results": results,
        "average_score": average_score
    }


def calculate_score(expected_diseases: Dict[str, float], submitted_diseases: Dict[str, float]) -> float:
    total_score = 0
    total_weight = sum(expected_diseases.values())

    for disease, expected_prob in expected_diseases.items():
        submitted_prob = submitted_diseases.get(disease, 0)
        difference = abs(expected_prob - submitted_prob)
        score_for_disease = (1 - difference) * (expected_prob / total_weight)
        total_score += score_for_disease

    return total_score * 100
