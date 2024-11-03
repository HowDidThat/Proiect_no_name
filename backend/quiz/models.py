from django.db import models
from authentication.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quiz_type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserQuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.JSONField()
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
