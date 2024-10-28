from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class QuizType(Enum):
    DISEASE_TO_SYMPTOMS = "disease_to_symptoms"
    SYMPTOMS_TO_DISEASE = "symptoms_to_disease"


class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class User(AbstractUser):
    institution = models.CharField(max_length=255)
    year_of_study = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField()
    correct_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserQuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
