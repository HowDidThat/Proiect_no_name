#-*- coding: utf-8 -*-

from django.db import models

class User(models.Model):
    class Meta:
        pass

    UserID = models.IntegerField()
    UserName = models.CharField()
    Email = models.CharField()
    Password = models.CharField()


    def login(self, ):
        pass

    def logout(self, ):
        pass

    def updateProfile(self, ):
        pass

