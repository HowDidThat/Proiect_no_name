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
        total_score = 0
     
        for i,key in enumerate(payload.answers[0].keys()):
            user_answer = payload.answers[0][key]
            question = quiz.questions[i]
            user_diseases = user_answer
            actual_diseases = question.get('diseases', {})

            all_probabilities = list(actual_diseases.values())
            all_probabilities.sort(reverse=True)

            max_score = sum(all_probabilities[:2]) / 2

            min_score = sum(all_probabilities[-2:]) / 2

            user_probabilities = [actual_diseases[disease] for disease in user_diseases if disease in actual_diseases]
            if not user_probabilities:
                question_score = 0
            else:
                avg_probability = sum(user_probabilities) / len(user_probabilities)

                scaled_score = ((avg_probability - min_score) / (
                            max_score - min_score)) * 100 if max_score != min_score else 0

                num_answers = len(user_diseases)
                if num_answers == 2:
                    multiplier = 1.0
                elif num_answers == 1:
                    multiplier = 0.8
                else:
                    multiplier = 0.7

                question_score = scaled_score * multiplier

            question_score = max(0, min(100, question_score))
            total_score += question_score
      
        final_score = round(total_score / len(quiz.questions), 2)

        UserQuizProgress.objects.create(
            user=request.user,
            quiz=quiz,
            answers=payload.answers,
            score=final_score
        )

        return 200, {"score": final_score}

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
