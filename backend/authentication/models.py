from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    institution = models.CharField(max_length=255)
    year_of_study = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'
