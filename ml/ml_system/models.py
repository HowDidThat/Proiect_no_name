from collections import OrderedDict

from django.db import models


class PredictionCache(models.Model):
    symptoms_hash = models.CharField(max_length=64, unique=True)
    predictions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prediction_cache'
