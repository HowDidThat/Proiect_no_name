from django.db import models
from enum import Enum


class QuizType(Enum):
    DISEASE_TO_SYMPTOMS = "disease_to_symptoms"
    SYMPTOMS_TO_DISEASE = "symptoms_to_disease"


class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quiz_type = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in QuizType]
    )
    difficulty = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in DifficultyLevel]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_quiz'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_question'
