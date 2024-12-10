#-*- coding: utf-8 -*-

from django.db import models

class Quiz(models.Model):
    class Meta:
        pass

    QuestionList = []
    QuestionsAnswered = models.IntegerField()
    Difficulty = models.IntegerField()


    def method(self, type):
        pass

