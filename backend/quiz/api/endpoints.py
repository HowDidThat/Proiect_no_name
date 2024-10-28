from ninja import NinjaAPI
from typing import List
from .schemas import (
    QuizSchema,
    QuizStartRequest,
    QuizSubmitRequest,
    ProgressSchema
)
from ..services.quiz_facade import QuizSystemFacade

api = NinjaAPI()


@api.get("/quizzes", response=List[QuizSchema])
def list_quizzes(request):
    # Implementation
    pass


@api.get("/quiz/{quiz_id}", response=QuizSchema)
def get_quiz(request, quiz_id: int):
    # Implementation
    pass


@api.post("/quiz/start")
def start_quiz(request, payload: QuizStartRequest):
    facade = QuizSystemFacade()  # Initialize with dependencies
    return facade.start_quiz(
        request.user.id,
        payload.quiz_type,
        payload.difficulty
    )


@api.post("/quiz/{quiz_id}/submit")
def submit_quiz(request, quiz_id: int, payload: QuizSubmitRequest):
    facade = QuizSystemFacade()  # Initialize with dependencies
    return facade.submit_quiz(
        request.user.id,
        quiz_id,
        payload.answers
    )


@api.get("/progress/{user_id}", response=List[ProgressSchema])
def get_user_progress(request, user_id: int):
    # Implementation
    pass
