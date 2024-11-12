from django.db import models


class MLModel(models.Model):
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50)
    model_path = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ml_model'


class PredictionLog(models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    input_data = models.JSONField()
    output_data = models.JSONField()
    confidence_score = models.FloatField()
    prediction_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prediction_log'