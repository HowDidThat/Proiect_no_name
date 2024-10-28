from abc import ABC, abstractmethod
from ..models import Quiz, QuizType


class QuizFactory(ABC):
    @abstractmethod
    def create_quiz(self, difficulty: str) -> Quiz:
        pass


class DiseaseToSymptomsQuizFactory(QuizFactory):
    def create_quiz(self, difficulty: str) -> Quiz:
        return Quiz(
            title=f"Disease to Symptoms - {difficulty}",
            quiz_type=QuizType.DISEASE_TO_SYMPTOMS.value,
            difficulty=difficulty
        )


class SymptomsToDiseaseQuizFactory(QuizFactory):
    def create_quiz(self, difficulty: str) -> Quiz:
        return Quiz(
            title=f"Symptoms to Disease - {difficulty}",
            quiz_type=QuizType.SYMPTOMS_TO_DISEASE.value,
            difficulty=difficulty
        )
