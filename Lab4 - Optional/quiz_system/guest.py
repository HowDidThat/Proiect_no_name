#-*- coding: utf-8 -*-

from django.db import models

from user import User

class Guest(User):
    class Meta:
        pass

    LastQuiz = None


    def takeQuiz(self, ):
        pass

    def submitQuiz(self, ):
        pass

    def checkQuiz(self, ):
        pass

