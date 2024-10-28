from typing import List, Dict
from .progress_tracker import ProgressSubject
from .quiz_factory import QuizFactory
from .quiz_evaluator import QuizEvaluationStrategy


class QuizSystemFacade:
    def __init__(
            self,
            quiz_factory: QuizFactory,
            evaluation_strategy: QuizEvaluationStrategy,
            progress_subject: ProgressSubject
    ):
        self.quiz_factory = quiz_factory
        self.evaluation_strategy = evaluation_strategy
        self.progress_subject = progress_subject

    def start_quiz(self, user_id: int, quiz_type: str, difficulty: str) -> Dict:
        quiz = self.quiz_factory.create_quiz(difficulty)
        return {
            "quiz_id": quiz.id,
            "questions": self._prepare_questions(quiz)
        }

    def submit_quiz(self, user_id: int, quiz_id: int, answers: Dict) -> Dict:
        correct_answers = self._get_correct_answers(quiz_id)
        score = self.evaluation_strategy.evaluate(answers, correct_answers)
        self._save_progress(user_id, quiz_id, score)
        self.progress_subject.notify(user_id, quiz_id, score)

        return {
            "score": score,
            "feedback": self._generate_feedback(score, answers),
            "recommendations": self._get_recommendations(user_id, score)
        }

    def _prepare_questions(self, quiz) -> List[Dict]:
        # Implementation to prepare questions
        pass

    def _get_correct_answers(self, quiz_id: int) -> Dict:
        # Implementation to get correct answers
        pass

    def _save_progress(self, user_id: int, quiz_id: int, score: float):
        # Implementation to save progress
        pass

    def _generate_feedback(self, score: float, answers: Dict) -> str:
        # Implementation to generate feedback
        pass

    def _get_recommendations(self, user_id: int, score: float) -> List[Dict]:
        # Implementation to get recommendations
        pass
