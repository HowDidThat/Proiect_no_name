#-*- coding: utf-8 -*-

from django.db import models

from user import User

class UserProfile(User):
    class Meta:
        pass

    QuizzesTaken = []
    AverageQuizPoints = models.DecimalField()
    Age = models.IntegerField()
    FacultyYear = models.IntegerField()


    def takeQuiz(self, ):
        pass

    def submitQuiz(self, ):
        pass

    def checkQuiz(self, ):
        pass

