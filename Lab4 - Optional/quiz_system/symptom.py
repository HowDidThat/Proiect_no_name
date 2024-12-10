#-*- coding: utf-8 -*-

from django.db import models

class Symptom(models.Model):
    class Meta:
        pass

    SymptopName = models.CharField()
    Difficulty = models.IntegerField()


