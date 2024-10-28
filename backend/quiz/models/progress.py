from django.db import models
from .user import User
from .quiz import Quiz


class UserQuizProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_progress')
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz_user_progress'
