#-*- coding: utf-8 -*-

from django.db import models

class Disease(models.Model):
    class Meta:
        pass

    DiseaseName = models.CharField()
    Difficulty = models.IntegerField()


