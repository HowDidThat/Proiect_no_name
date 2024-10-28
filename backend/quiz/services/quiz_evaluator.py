from abc import ABC, abstractmethod


class QuizEvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self, user_answers: dict, correct_answers: dict) -> float:
        pass


class BasicEvaluationStrategy(QuizEvaluationStrategy):
    def evaluate(self, user_answers: dict, correct_answers: dict) -> float:
        correct_count = 0
        total_questions = len(correct_answers)

        for question_id, correct_answer in correct_answers.items():
            user_answer = user_answers.get(question_id)
            if user_answer == correct_answer:
                correct_count += 1

        return (correct_count / total_questions) * 100


class KeywordEvaluationStrategy(QuizEvaluationStrategy):
    def evaluate(self, user_answers: dict, correct_answers: dict) -> float:
        # Implementation for keyword-based evaluation
        pass
